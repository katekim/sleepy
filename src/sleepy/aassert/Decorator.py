from Var import Var
import Conds

class Decorator:

    var = Var

    def __call__ (self, *validators):

        def dec (fn):

            def wrapped (*args, **kwargs):
                args = list (args)
                for v in validators:
                    v.validate (fn, args, kwargs)
                    pass

                return fn (*args, **kwargs)

            return wrapped

        return dec

    def __getattr__ (self, name):
        if name in Conds.conds:
            return lambda *args, **kwargs: self._call (name, args, kwargs)
        else:
            raise AttributeError (name)
        pass

    def _call (self, name, args, kwargs):
        return Conds.conds[name] (*args, **kwargs)
    
    pass
