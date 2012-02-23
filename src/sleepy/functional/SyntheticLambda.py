import sleepy

class Term: pass

class Value (Term):

    def __init__ (self, value):
        self.value = value
        pass

    def __repr__ (self):
        return "Value(%s)" % self.value

    pass

class ValueList (Term):

    def __init__ (self, values):
        self.values = sleepy.collection.List.fromIterator (values)
        pass

    def __repr__ (self):
        return "ValueList(%s)" % self.values

    pass

#
# CallTerm represents calling a function.  Calling a method is
# represented as a combination of GetAttrTerm and CallTerm.  However,
# before evaluation phase, the combination is converted to a single
# CallFuncTerm so that calling a method can return a ValueWrapper
# object.  So, CallTerm will never be used in the evaluation phase.
#
class CallTerm (Term):

    def __init__ (self, func, args = (), kwargs = {}):
        self.func = func
        self.args = ValueList (map (Value, args))
        self.kwargs = sleepy.collection.Map.fromDict (kwargs)
        pass

    def __repr__ (self):
        p = sleepy.collection.MList ()
        if not self.args.values.isEmpty:
            p <<= ", ".join (self.args.values.map (str))
            pass

        if not self.kwargs.isEmpty:
            p <<= ", ".join (self.kwargs.items.map (lambda (k, v): "%s=%s" % (str (k), str (v))))
            pass

        return "Call(%s, %s)" % (self.func, self.args)

    pass

class CallFuncTerm (Term):

    def __init__ (self, func, args):
        self.func = func
        self.args = args
        pass

    def __repr__ (self):
        return "CallFunc(%s, %s)" % (self.func, self.args)

    pass

class CallUserDefinedFuncTerm (Term):

    def __init__ (self, func, args, kwargs):
        self.func = func
        self.args = ValueList (map (Value, args))
        self.kwargs = kwargs
        pass

    def __repr__ (self):
        return "CallUserDefinedFuncTerm(%s)" % (self.func)

    pass

class CmpTerm (Term):

    def __init__ (self, o):
        self.o = Value (o)
        pass

    def __repr__ (self):
        return "Cmp(%s)" % self.o

    pass

class GetAttrTerm (Term):

    def __init__ (self, name):
        self.name = name
        pass

    def __repr__ (self):
        return "GetAttr(%s)" % self.name

    pass

class IfTerm (Term):

    def __init__ (self, cond, then, _else):
        self.cond = Value (cond)
        self.then = Value (then)
        self._else = Value (_else)
        pass

    def __repr__ (self):
        return "If(%s, %s, %s)" % (self.cond, self.then, self._else)

    pass

class IntervalTerm (Term):

    def __init__ (self, a, b, type):
        self.a = Value (a)
        self.b = Value (b)
        self.type = type
        pass

    def __repr__ (self):
        return "Interval(%s, %s, %s)" % (self.a, self.b, self.type)

    pass

class LogOpTerm (Term):

    def __init__ (self, type, xs):
        self.type = type
        self.xs = sleepy.collection.List.fromIterator (xs).map (Value)
        pass

    def __repr__ (self):
        return "LogOp(%s, %s)" % (self.type, ", ".join (self.xs.map (str)))

    pass


class Recordable: pass

class Recorder (Recordable):

    def __init__ (self, data = sleepy.collection.List ()):
        self._sl_data = sleepy.collection.MList.fromIterator (data)
        pass

    def _sl_getattr (self):
        return self._sl_data[0].name if (self._sl_data.length == 1) and (isinstance (self._sl_data[0], GetAttrTerm)) else \
               None

    def cmp_ (self, o):
        self._sl_data <<= CmpTerm (o)
        return self

    def if_ (self, cond, then, _else):
        self._sl_data <<= IfTerm (cond, then, _else)
        return self

    def __call__ (self, *args, **kwargs):
        self._sl_data <<= CallTerm ("__call__", args, kwargs)
        return self

    def __coerce__ (self, op1):
        return None

    def __getattr__ (self, name):
        self._sl_data <<= GetAttrTerm (name)
        return self

    def __repr__ (self):
        return "x." + ".".join (self._sl_data.map (str))

    def __str__ (self):
        return repr (self)

    def and_ (self, *xs):
        self._sl_data <<= LogOpTerm ("and", xs)
        return self

    def not_ (self, x):
        self._sl_data <<= LogOpTerm ("not", [x])
        return self

    def or_ (self, *xs):
        self._sl_data <<= LogOpTerm ("or", xs)
        return self

    def xor_ (self, a, b):
        self._sl_data <<= LogOpTerm ("xor", [a, b])
        return self

    def cc_ (self, a, b):
        self._sl_data <<= IntervalTerm (a, b, "cc")
        return self

    def co_ (self, a, b):
        self._sl_data <<= IntervalTerm (a, b, "co")
        return self

    def oc_ (self, a, b):
        self._sl_data <<= IntervalTerm (a, b, "oc")
        return self

    def oo_ (self, a, b):
        self._sl_data <<= IntervalTerm (a, b, "oo")
        return self

    def f_ (self, func):

        def f (*args, **kwargs):
            self._sl_data <<= CallUserDefinedFuncTerm (func, args, kwargs)
            return self

        return f

    def _lmd (self, nargs, vnames = []):
        return Evaluator ().eval (self, nargs, vnames)

    pass

class Recorder0 (Recordable):

    Redirects = ["and_", "not_", "or_", "xor_",
                 "cc_", "oc_", "co_", "oo_", "f_",
                 "if_", "_lmd"]

    def __init__ (self):
        self._sl_data = sleepy.collection.List ()
        pass

    def __call (self, name, args, kwargs):
        return getattr (Recorder (), name) (*args, **kwargs)

    def __getattr__ (self, name):
        if name in Recorder0.Redirects:
            return lambda *args, **kwargs: self.__call (name, args, kwargs)
        else:
            return Recorder ().__getattr__ (name)

    def __coerce__ (self, op1):
        return None

    def __repr__ (self):
        return "x"

    def __str__ (self):
        return repr (self)

    pass

class Formatter:

    def __init__ (self, recorder):
        self._recorder = recorder
        pass

    def __repr__ (self):
        return "x." + ".".join (self._recorder._data.map (str))

    pass

class Params:
    
    def __init__ (self, var):
        self._var = var
        self._data = sleepy.collection.MList ()
        pass

    def _alt_cmp (self, op, x):
        return lambda x: True

    def __getitem__ (self, n):
        return self._data[n]

    def __call__ (self, value):
        self._data <<= value
        return "%s[%d]" % (self._var, self._data.length - 1)

    def __repr__ (self):
        return repr (self._data)

    pass

#
# ValueWrapper wraps a value so that the value can be pretended to
# have special methods like _sl_call() and _sl_cmp().
#
# Any method calls should return a value as a ValueWrapper unless it
# returns None.
#
# ValueWrapper is instantiated when the input variables are used, a
# method returns, and a named variable is used.
#
class ValueWrapper:

    AlternativeCmp = {'__eq__' : lambda x : x == 0,
                      '__ne__' : lambda x : x != 0,
                      '__lt__' : lambda x : x < 0,
                      '__le__' : lambda x : x <= 0,
                      '__gt__' : lambda x : x > 0,
                      '__ge__' : lambda x : x >= 0,
                      }

    def __init__ (self, value, vnames = []):
        self._vmap = vnames
        self.vnames = vnames
        self.value = value
        pass

    def _sl_call (self, func, args):
        args = sleepy.collection.List.fromIterator (args)
        args = args.map (lambda x: x.value if isinstance (x, ValueWrapper) else x)

        return self._sl_cmpop (func, args[0]) if func in ValueWrapper.AlternativeCmp else \
               ValueWrapper (getattr (self.value, func) (*args))

    def _sl_cmpop (self, func, arg):
        return ValueWrapper (getattr (self.value, func) (arg) if hasattr (self.value, func) else \
                             ValueWrapper.AlternativeCmp[func] (cmp (self.value, arg)))

    def _sl_cmp (self, o):
        if hasattr (self, "__cmp__"):
            ret = cmp (self.value, o)
        else:
            ret = -1 if self.value < o  else \
                  0  if self.value == o else \
                  1
            pass

        return ret

    def _sl_call_ud (self, func, args):
        return ValueWrapper (func (*args))

    def _sl_if (self, eval1, x, cond, then, _else):
        sleepy._debug ("_sl_if", eval1, x, cond, then, _else)
        result = then if cond else _else
        val = eval1 (sleepy.collection.List (result), -1, []) (*x) if type (x) is tuple else \
              eval1 (sleepy.collection.List (result), 1, []) (x)
        return ValueWrapper (val)

    def _sl_interval (self, a, b, type):
        return a <= self.value <= b if type == "cc" else \
               a <  self.value <= b if type == "oc" else \
               a <= self.value <  b if type == "co" else \
               a <  self.value <  b if type == "oo" else \
               None

    def _sl_logop (self, eval1, input, typ, xs):
        sleepy._debug ("_sl_logop", typ, xs)

        def eval2 (x):
            return eval1 (sleepy.collection.List (x), -1, []) (*input) if type (input) is tuple else \
                   eval1 (sleepy.collection.List (x), 1, []) (input)

        if typ == "and":
            ret = True
            for x in xs:
                if not eval2 (x):
                    ret = False
                    break
                pass
            pass
        elif typ == "or":
            ret = False
            for x in xs:
                if eval2 (x):
                    ret = True
                    break
                pass
            pass
        elif typ == "xor":
            a = eval2 (xs[0])
            b = eval2 (xs[1])
            ret = ((a is True) and (b is False)) or ((a is False) and (b is True))
        elif typ == "not":
            ret = not eval2 (xs[0])
        else:
            raise ValueError

        return ret

    def _sl_getattr (self, name):
        return getattr (self, name)

    def __getattr__ (self, name):
        if name in self._vmap:
            v = self.value[self._vmap.index (name)] if type (self.value) is tuple else \
                self.value
            return ValueWrapper (v, self.vnames)
        elif name in ('__call__', '__repr__', '__str__'):
            return getattr (self.value, name)
        else:
            return ValueWrapper (getattr (self.value, name))
        pass

    pass

class Evaluator:
    
    def optimise (self, terms):

        def loop (terms, prev = None, terms1 = sleepy.collection.List ()):
            if terms.isEmpty:
                return terms1
            else:
                if isinstance (prev, GetAttrTerm) and isinstance (terms.head, CallTerm):
                    return loop (terms.tail, None, terms1.take (terms1.length - 1) << CallFuncTerm (prev.name, terms.head.args))
                else:
                    return loop (terms.tail, terms.head, terms1 << terms.head)
                pass
            pass

        return loop (terms)

    def eval (self, terms, nargs, vnames):

        def eval1 (term):
            if isinstance (term, Recordable):
                sleepy._debug ( "Recordable", term.__dict__['_sl_data'])
                return "ValueWrapper (x, vnames)" + eval1 (term.__dict__['_sl_data'])
            elif isinstance (term, sleepy.collection.Sequential):
                return "".join (self.optimise (term).map (eval1))
            elif isinstance (term, CallTerm):
                return "(*[%s])" % ", ".join (eval1 (term.args).map (str))
            elif isinstance (term, CallFuncTerm):
                sleepy._debug ("CallFunc", eval1 (term.args))
                return "._sl_call ('%s', [%s])" % (term.func, ", ".join (eval1 (term.args).map (str)))
            elif isinstance (term, CallUserDefinedFuncTerm):
                return "._sl_call_ud (%s, [%s])" % (p (term.func), ", ".join (eval1 (term.args).map (str)))
            elif isinstance (term, CmpTerm):
                return "._sl_cmp (%s)" % eval1 (term.o)
            elif isinstance (term, GetAttrTerm):
                return "._sl_getattr ('%s')" % term.name
            elif isinstance (term, IfTerm):
                return "._sl_if (%s, x, %s, %s, %s)" % (p (self.eval), eval1 (term.cond), p (term.then), p (term._else))
            elif isinstance (term, IntervalTerm):
                return "._sl_interval (%s, %s, '%s')" % (eval1 (term.a), eval1 (term.b), term.type)
            elif isinstance (term, LogOpTerm):
                return "._sl_logop (%s, x, '%s', %s)" % (p (self.eval), term.type, p (term.xs))
            elif isinstance (term, Value):
                return eval1 (term.value) if isinstance (term.value, Recordable) else \
                       p (term.value)
            elif isinstance (term, ValueList):
                return term.values.map (eval1)
            else:
                raise ValueError (term)
            pass

        def strip (x):
            return x.value if isinstance (x, ValueWrapper) else x

        p = Params ("__sl_p")
        args = "x" if nargs == 1 else "*x"
        s = ("lambda __sl_p, vnames, _sl_strip: lambda %s: _sl_strip (" % args) + eval1 (terms) + ")"

        sleepy._debug (s)
        sleepy._debug (p)
        return eval (s) (p, vnames, strip)

    pass

class SyntheticLambda:
    
    @staticmethod
    def fn (*nargs):

        def wrap (decos, fn):
            decos = sleepy.collection.List.fromIterator (decos)
            return decos.fold (fn, lambda fn, deco: deco (fn))

        nargs = sleepy.collection.List.fromIterator (nargs)
        if not nargs.isEmpty and nargs.forall (lambda x: isinstance (x, Recordable) or (type (x) is str)):
            return lambda *xs: wrap (xs[:-1],
                                     xs[-1]._lmd (nargs.length,
                                                  nargs.map (lambda y: y._sl_getattr () if isinstance (y, Recordable) else y)))
        elif nargs.length == 1:
            return lambda *xs: wrap (xs[:-1],
                                     xs[-1]._lmd (nargs[0]) if isinstance (xs[-1], Recordable) else \
                                     lambda *dummy: xs[-1])
        else:
            raise ValueError ("nargs should be a list of integers or a list of Recorders.")

        pass

    @staticmethod
    def _fn (lmd, nargs = 1):
        if isinstance (lmd, Recordable):
            f0 = lmd._lmd (nargs)
            def f (*args):
                ret = f0 (args[0]) if nargs == 1 else \
                      f0 (*args)

                return ret.value if isinstance (ret, ValueWrapper) else \
                       ret

            return f
        else:
            return lmd
        pass

    def __init__ (self, nargs, recorder):
        self._nargs = nargs
        self._recorder = recorder
        pass
    
    def __repr__ (self):
        return repr (Formatter (self._recorder))

    def __str__ (self):
        return repr (self)
