import sleepy
from Sequential import MSequential, Sequential
from ..aassert import Decorator
aa = Decorator ()

class List (Sequential):

    def __init__ (self, *lis):
        self._lis = list (lis)
        pass

    def __iter__ (self):
        return iter (self._lis)

    def __len__ (self):
        return len (self._lis)

    @aa (aa.var ("n").ofType (int))
    def __getitem__ (self, n):
        return self._lis[n]

    def __create__ (self, it):
        return List.fromIterator (it)

    def __repr__ (self):
        return 'List(%s)' % ', '.join (map (str, self._lis))

    pass


class MList (MSequential):

    def __init__ (self, *xs):
        self._lis = list (xs)
        pass

    def __append__ (self, v):
        self._lis.append (v)
        pass

    @aa (aa.var ("n").ofType (int))
    def __setitem__ (self, n, v):
        self._lis[n] = v
        pass

    def __iter__ (self):
        return iter (self._lis)

    def __len__ (self):
        return len (self._lis)

    def __getitem__ (self, n):
        return self._lis[n]

    def __create__ (self, it):
        return MList.fromIterator (it)

    def __repr__ (self):
        return 'MList(%s)' % ', '.join (map (str, self._lis))

    pass
