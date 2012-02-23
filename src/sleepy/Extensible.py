class Extensible:

    prototype = {}

    def __init__ (self):
        pass

    def __getattr__ (self, name):
        if name in self.prototype:
            if hasattr (self.prototype[name], '__call__'):
                return lambda *args, **kwargs: self.prototype[name] (self, *args, **kwargs)
            else:
                return self.prototype[name]
            pass
        else:
            return self.__getattr_local__ (name)

    pass

