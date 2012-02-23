class Maybe:

    def getOrElse (self, default = None):
        try:
            ret = self.get ()
        except ValueError:
            ret = default
            pass

        return ret

    @property
    def isEmpty (self):
        try:
            self.get ()
            return False
        except ValueError:
            return True
        pass

    @property
    def nonEmpty (self):
        return not self.isEmpty

    pass

class Just (Maybe):

    def __init__ (self, value):
        self.value = value
        pass

    def __iter__ (self):
        return iter ([self.value])

    def get (self):
        return self.value

    pass


class _Nothing (Maybe):

    def __iter__ (self):
        return iter ([])

    def get (self):
        raise ValueError ("Nothing contains no value.")

    pass

Nothing = _Nothing ()
