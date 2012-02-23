class Val:

    def __init__ (self):
        self.__dict__["_values"] = {}
        pass

    def __getattr__ (self, key):
        if key in self.__dict__["_values"]:
            return self.__dict__["_values"][key]
        else:
            raise AttributeError (key)
        pass

    def __setattr__ (self, key, value):
        if key in self.__dict__["_values"]:
            raise ValueError ("%s: assignment not allowed" % key)
        else:
            self.__dict__["_values"][key] = value
            pass
        pass

    pass
