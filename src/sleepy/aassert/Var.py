import inspect
from AaValueError import *
import Conds

class Var:

    def __init__ (self, name):
        self._name = name
        self._conds = []
        pass

    def getArgs (self, argspec, args):
        if argspec.defaults is None:
            return args
        else:
            return list (args) + list (argspec.defaults)[len (argspec.defaults) - len (argspec.args) + len (args):]
        pass

    def getArg (self, fn, args):
        argspec = inspect.getargspec (fn)
        if self._name not in argspec.args:
            raise ValueError ("Argument `%s' is undefined." % self._name)

        ndefaults = len (argspec.args) - len (args)
        for i in range (ndefaults):
            args.append (argspec.defaults[len (argspec.defaults) - ndefaults + i])
            pass

        i = argspec.args.index (self._name)
        v = args[i]
        setter = lambda x: args.__setitem__ (i, x)
        return v, setter

    def validate (self, fn, args, kwargs):
        try:
            v, setter = self.getArg (fn, args)
            for cond in self._conds:
                ret = cond.validate (self._name, v)
                if ret is not None:
                    setter (ret)
                    pass
                pass
            pass
        except AaValueError as e:
            s = msgs["exc.format"] % dict (name = self._name,
                                           expected = "`%s' to be %s" % (self._name, e.expected % dict (name = "`%s'" % self._name)),
                                           actual = e.actual % dict (name = "`%s'" % self._name))
            raise ValueError (s)
        pass

    def __getattr__ (self, name):
        lastCond = self._conds[-1] if len (self._conds) > 0 else None

        if not isinstance (lastCond, Conds.Redirectable) and (name in Conds.conds):
            def _call (name, args, kwargs):
                self._conds.append (Conds.conds[name] (*args, **kwargs))
                return self

            return lambda *args, **kwargs: _call (name, args, kwargs)
        elif isinstance (lastCond, Conds.Redirectable) and hasattr (self._conds[-1], name):
            def _call (name, args, kwargs):
                getattr (self._conds[-1], name) (*args, **kwargs)
                return self

            return lambda *args, **kwargs: _call (name, args, kwargs)
        else:
            raise AttributeError (name)
        pass

    def __repr__ (self):
        return ("var(%s)." % self._name) + ".".join (map (repr, self._conds))

    pass

