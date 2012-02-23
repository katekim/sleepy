from Iterable import Iterable

class Set (Iterable):

    def __init__ (self, *lis):
        self._set = set (lis)
        pass

    def __iter__ (self):
        return iter (self._set)

    def __contains__ (self, x):
        return x in self._set

    def isDisjoint (self, o):
        return self._set.isdisjoint (o)

    def length (self):
        return len (self._set)

    pass
