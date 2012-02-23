import sleepy
from Iterable import Iterable
from ..aassert import Decorator
aa = Decorator()

class Sequential(Iterable):

    @classmethod
    def fromIterator(cls, it):
        lis = list(it)
        return cls(*lis)

    def __len__(self):
        raise NotImplemented("__len__")

    def __getitem__(self, n):
        raise NotImplemented("__getitem__")

    @aa(aa.var("n").ofType(int),
        aa.var("m").ofType(int))
    def __getslice__(self, n, m):
        lis = []
        for i in range(n, min(m, len(self))):
            lis.append(self[i])
            n += 1

        return self.__create__(iter(lis))

    def __add__(self, o):
        return self.concat(o)

    def __iadd__(self, o):
        raise ValueError("%s is immutable." % self.__class__.__name__)

    def __ilshift__(self, x):
        raise ValueError("%s is immutable." % self.__class__.__name__)

    def __lshift__(self, o):
        return self.append(o)

    def __rrshift__(self, o):
        return self.prepend(o)

    def append(self, *xs):
        lis = self[:].toBuiltinList()
        for x in xs:
            lis.append(x)

        return self.__create__(iter(lis))

    @aa(aa.var("o").iterable())
    def concat(self, o):
        lis = []

        for x in self:
            lis.append(x)

        for x in o:
            lis.append(x)

        return self.__create__(iter(lis))

    def contains(self, x):
        return(x in self.toBuiltinList())

    @aa(aa.var("lis").iterable())
    def endsWith(self, lis):
        if self.length < lis.length:
            return False

        return lis.reverse().zip(self.reverse()).forall(lambda x: x[0] == x[1])

    def flatten(self):
        ret = []
        for lis in self:
            for x in lis:
                ret.append(x)

        return self.__create__(iter(ret))

    def prepend(self, *xs):
        lis = list(xs)
        for x in self:
            lis.append(x)

        return self.__create__(iter(lis))

    @property
    def head(self):
        return self[0]

    def index(self, v):
        return self.toBuiltinList().index(v)

    @property
    def isEmpty(self):
        return self.length == 0

    @property
    def nonEmpty(self):
        return not self.isEmpty

    @property
    def last(self):
        if self.isEmpty:
            raise IndexError

        return self[self.length - 1]

    def reverse(self):
        lis = self.toBuiltinList()
        lis.reverse()
        return self.__create__(iter(lis))

    @property
    def length(self):
        return len(self)

    @aa(aa.var("lis").iterable())
    def startsWith(self, lis):
        if self.length < lis.length:
            return False

        return lis.zip(self).forall(lambda x: x[0] == x[1])

    @aa(aa.var("cmp").callable())
    def sort(self, cmp = lambda a, b: cmp(a, b)):
        cmp = sleepy.functional.SyntheticLambda._fn(cmp, 2)
        lis = self.toBuiltinList()
        lis.sort(cmp)
        return self.__create__(iter(lis))

    @property
    def tail(self):
        if self.isEmpty:
            raise IndexError("tail() called with an empty list")

        lis = self.toBuiltinList()
        return self.__create__(iter(lis[1:]))


class MSequential(Sequential):

    def __append__(self, x):
        raise NotImplemented("__append__")

    def __ilshift__(self, x):
        self.appendD(x)
        return self

    def __setitem__(self, n, value):
        raise NotImplemented("__setitem__")

    @aa(aa.var("cmp").callable())
    def sortD(self, cmp = lambda a, b: cmp(a, b)):
        lis = self.toBuiltinList()
        cmp = sleepy.functional.SyntheticLambda._fn(cmp, 2)
        lis.sort(cmp)
        for i in range(len(lis)):
            self[i] = lis[i]

    def appendD(self, *xs):
        for x in xs:
            self.__append__(x)

    def reverseD(self):
        lis = self.toBuiltinList()
        lis.reverse()
        for i in range(len(lis)):
            self[i] = lis[i]
