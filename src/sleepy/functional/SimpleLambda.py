import copy, re, time

class Evaluator:

    def __init__ (self, lmd, x):
        self._lmd = lmd
        self._x = x
        pass

    def replaceSimpleLambda (self, args, kwargs):
        for i in range (len (args)):
            if isinstance (args[i], SimpleLambda):
                args[i] = args[i] (self._x)
                pass
            pass

        for k in kwargs:
            if isinstance (kwargs[k], SimpleLambda):
                kwargs[k] = kwargs[k] (self._x)
                pass
            pass
        pass

    def evalOne (self, finfo, x):
        args, kwargs = copy.copy (finfo['args']), copy.copy (finfo['kwargs'])
        self.replaceSimpleLambda (args, kwargs)
        if hasattr (finfo['fn'], '__call__'):
            val = finfo['fn'] (x)
        elif (finfo['fn'] in SimpleLambda.AlternativeCmp) and not hasattr (x, '__eq__'):
            val = SimpleLambda.AlternativeCmp[finfo['fn']] (getattr (x, '__cmp__') (*args, **kwargs))
        else:
            val = getattr (x, finfo['fn']) (*args, **kwargs)
            pass

        return val

    def eval (self):
        y = self.evalOne (self._lmd._fn[0], self._x)
        for fn in self._lmd._fn[1:]:
            y = self.evalOne (fn, y)
            pass

        return y

    pass

class SpecialExpression:
    pass

class IfExpression (SpecialExpression):

    def __init__ (self, cond, _then, _else):
        self._cond = cond
        self._then = _then
        self._else = _else
        print 'IfExpression', cond, _then, _else
        pass

    pass

class SimpleLambda:

    BinaryOperators = {'__add__' : '+',
                       '__radd__' : '+',
                       '__sub__' : '-',
                       '__rsub__' : '-',
                       '__mul__' : '*',
                       '__rmul__' : '*',
                       '__div__' : '/',
                       '__rdiv__' : '/',
                       '__eq__' : '==',
                       '__ne__' : '!=',
                       '__lt__' : '<',
                       '__le__' : '<=',
                       '__gt__' : '>',
                       '__ge__' : '>=',
                       }

    AlternativeCmp = {'__eq__' : lambda x : x == 0,
                      '__ne__' : lambda x : x != 0,
                      '__lt__' : lambda x : x < 0,
                      '__le__' : lambda x : x <= 0,
                      '__gt__' : lambda x : x > 0,
                      '__ge__' : lambda x : x >= 0,
                      }
                       
    def __init__ (self):
        self._fn = []
        self._repr = []
        self._lambda = None
        pass

    def _lmd_getattr (self, name):
        if name == '__call__':
            return lambda *args, **kwargs: self (*args, **kwargs)
        else:
            return (lambda name: lambda *args, **kwargs: self._lmd_call (name, args, kwargs)) (name)
        pass

    def _lmd_call (self, name, args, kwargs):
        self._fn.append ({'fn' : name, 'args' : list (args), 'kwargs' : kwargs})

        if name in SimpleLambda.BinaryOperators:
            self._repr.insert (0, '(x %s %s)' % (SimpleLambda.BinaryOperators[name], args[0]))
        else:
            sargs = re.sub (',$', '', str (args)[1:-1])
            skwargs = ', '.join ('%s=%s' % x for x in kwargs.items ())
            s = [sargs]
            if skwargs != '':
                s.append (skwargs)
                pass

            self._repr.insert (0, 'x.%s(%s)' % (name, ', '.join (s)))
            pass

        return self

    def __getattr__ (self, name):
        return (lambda name: lambda *args, **kwargs: self._lmd_call (name, args, kwargs)) (name)

    def __coerce__ (self, op1):
        return None

    def __sl_cmp (self, fn, a, b):
        if hasattr (a, fn):
            return getattr (a, fn) (b)
        else:
            return SimpleLambda.AlternativeCmp[fn] (cmp (a, b))
        pass

    def __createLambda (self, offset = 0):

        def buildArgs (args, idx, acc = [], vars = []):
            if len (args) == 0:
                return acc, vars
            elif isinstance (args[0][1], SimpleLambda):
                lmd1, vars1 = args[0][1].__createLambda (offset = idx)
                #print 'buildArgs', lmd1, vars1
                return buildArgs (args[1:],
                                  idx + len (vars1),
                                  acc + [lmd1],
                                  vars + vars1)
            else:
                acc1 = acc + ['__sl_vars[%d]' % idx] if args[0][0] == 'list' else \
                       acc + ['%s = __sl_vars[%d]' % (args[0][2], idx)]
                vars1 = vars + [args[0][1]] if args[0][0] == 'list' else \
                        vars + [args[0][1]]
                return buildArgs (args[1:], idx + 1, acc1, vars1)
            pass
        
        def buildLambda (fnlist, lmd = 'x', vars = []):
            if len (fnlist) == 0:
                return lmd, vars
            else:
                fn0 = fnlist[0]
                if fn0['fn'] in SimpleLambda.AlternativeCmp:
                    lmd0, vars0 = buildArgs ([('list', fn0['args'][0])], len (vars))
                    lmd1 = "__sl_cmp ('%s', %s, %s)" % (fn0['fn'], lmd, lmd0[0])
                    return buildLambda (fnlist[1:], lmd1, vars + vars0)
                elif isinstance (fn0['fn'], SpecialExpression):
                    print '==== special'
                    print fn0
                else:
                    arglist = [('list', x) for x in fn0['args']] + [('map', v, k) for k, v in fn0['kwargs'].items ()]
                    args, vars1 = buildArgs (arglist, len (vars) + offset, vars = vars)
                    return buildLambda (fnlist[1:],
                                        lmd + ".%s(%s)" % (fn0['fn'], ', '.join (args)),
                                        vars1)
                pass
            pass

        return buildLambda (self._fn)

    def __call__ (self, *x):
        #print '__call__', x

        if len (x) == 1:
            x = x[0]
            pass

        if len (self._fn) == 0:
            return x

        if self._lambda is None:
            lmd0, vars = self.__createLambda ()
            lmd = 'lambda __sl_vars: lambda x: ' + lmd0
            #print lmd.replace ('__sl_vars', 'a')
            self._lambda = eval (lmd, {'__sl_cmp' : self.__sl_cmp}) (vars)
            pass

        return self._lambda (x)

    def __repr__ (self):
        s = 'x'
        for x, r in zip (self._fn, self._repr):
            s = s.replace ('x', r, 1)
            pass

        return s

    __str__ = __repr__

    pass

class SimpleLambdaCreator:

    def __getattr__ (self, name):
        return SimpleLambda ()._lmd_getattr (name)

    def __coerce__ (self, op1):
        return None

    pass
