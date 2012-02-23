import sleepy
from Iterable import Iterable, IterableOnce
from List import List

class Seq (Iterable):

    @staticmethod
    def arith (a0, d):
        return Seq ((a0, None), lambda x: (x[0] + d, None))

    @staticmethod
    def geom (a0, r):
        return Seq ((a0, None), lambda x: (x[0] * r, None))

    def __create__ (self, it):
        return IterableOnce (it)

    def __init__ (self, a0, an):
        self._an1 = a0
        self._an = sleepy.functional.SyntheticLambda._fn (an)
        self._n = 0
        pass

    def __iter__ (self):
        return self

    def next (self):
        if self._n == 0:
            a = self._an1
        else:
            a = self._an (self._an1)
            pass

        self._an1 = a
        self._n += 1
        return a[0]

    pass
