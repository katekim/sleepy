import itertools
from ..aassert import Decorator
aa = Decorator ()

class Iterable:

    def __iter__ (self):
        raise NotImplemented ('__iter__')

    def __create__ (self, it):
        raise NotImplemented ('__create__')

    def __eq__ (self, o):
        if not isinstance (o, Iterable):
            return False

        slis = list (self)
        olis = list (o)

        if len (slis) != len (olis):
            return False

        return all (x[0] == x[1] for x in zip (slis, olis))

    def __ne__ (self, o):
        return not (self == o)

    @aa (aa.var ("p").callable ())
    def count (self, p):
        return self.filter (p).toList ().length

    @aa (aa.var ("n").or_ (aa.ofType (int)))
    def drop (self, n):

        def gen (it):
            for i in range (n):
                it.next ()
                pass

            for x in it:
                yield x
                pass
            pass

        return self.__create__ (gen (iter (self)))

    @aa (aa.var ("p").callable ())
    def dropWhile (self, p):
        from ..functional import SyntheticLambda
        p = SyntheticLambda._fn (p)
        return self.__create__ (itertools.dropwhile (p, self))

    @aa (aa.var ("p").callable ())
    def exists (self, p):
        return self.filter (p).toList ().length > 0

    @aa (aa.var ("p").callable ())
    def filter (self, p):
        from ..functional import SyntheticLambda
        p = SyntheticLambda._fn (p)
        return self.__create__ (itertools.ifilter (p, self))

    @aa (aa.var ("fn").callable ())
    def fold (self, x0, fn):
        from ..functional import SyntheticLambda
        fn = SyntheticLambda._fn (fn, 2)
        return reduce (fn, self, x0)

    @aa (aa.var ("p").callable ())
    def forall (self, p):
        from ..functional import SyntheticLambda
        p = SyntheticLambda._fn (p)
        return self.filter (lambda x: not p (x)).toList ().length == 0

    @aa (aa.var ("fn").callable ())
    def foreach (self, fn):
        from ..functional import SyntheticLambda
        fn = SyntheticLambda._fn (fn)
        for x in self:
            fn (x)
            pass
        pass

    @aa (aa.var ("fn").callable ())
    def map (self, fn):
        from ..functional import SyntheticLambda
        fn = SyntheticLambda._fn (fn)
        return self.__create__ (itertools.imap (fn, self))

    @property
    def min (self):
        return min (self)

    @property
    def max (self):
        return max (self)

    @aa (aa.var ("fn").callable ())
    def reduce (self, fn):
        from ..functional import SyntheticLambda
        fn = SyntheticLambda._fn (fn, 2)
        return reduce (fn, self)

    @property
    def sum (self):
        return sum (self)

    @property
    def product (self):
        lis = self.toList ()
        return 1 if lis.isEmpty else \
               self.reduce (lambda a, b: a * b)

    @aa (aa.var ("n").or_ (aa.ofType (int)))
    def take (self, n):
        def gen (it):
            for i in range (n):
                yield it.next ()
                pass
            pass

        return self.__create__ (gen (iter (self)))

    @aa (aa.var ("p").callable ())
    def takeWhile (self, p):
        from ..functional import SyntheticLambda
        p = SyntheticLambda._fn (p)
        return self.__create__ (itertools.takewhile (p, self))
    
    def toBuiltinList (self):
        return [x for x in self]

    def toList (self):
        from List import List
        return List.fromIterator (self)

    @property
    def unique (self):
        lis = []
        x0 = lambda : 0  # matches nothing
        for x in self:
            if not (x == x0):
                lis.append (x)
                x0 = x
                pass
            pass

        return self.__create__ (iter (lis))


    @property
    def unique0 (self):
        d = {}
        for x in self:
            d[x] = 1
            pass

        return self.__create__ (d.iterkeys ())

    def zip (self, *iterables):
        return self.__create__ (itertools.izip (self, *iterables))

    def zipFilled (self, *iterables, **kwargs):
        lis = [self] + list (iterables)
        return self.__create__ (itertools.izip_longest (*lis, fillvalue = kwargs.get ('fill', None)))

    pass

class IterableOnce (Iterable):

    def __init__ (self, it):
        self._it = it
        self._available = True
        pass

    def __create__ (self, it):
        return IterableOnce (it)

    def __iter__ (self):
        if not self._available:
            raise ValueError ("IterableOnce can only iterate once .")

        self._available = False
        return self._it

    pass
