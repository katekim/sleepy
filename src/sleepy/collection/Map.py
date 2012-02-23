import copy, sleepy

class MapLike:

    @classmethod
    def fromDict (cls, d):
        return cls (**d)

    def __getitem__ (self, key):
        raise NotImplemented ("__getitem__")

    def __iter__ (self):
        raise NotImplemented ("__iter__")
    
    def __add__ (self, o):
        return self.concat (o)

    def __len__ (self):
        return self.keys.length

    def __eq__ (self, o):
        if type (self) is not type (o):
            return False

        keys0 = sleepy.collection.MList.fromIterator (iter (self))
        keys0.sortD ()
        keys1 = sleepy.collection.MList.fromIterator (iter (o))
        keys1.sortD ()

        if keys0.length != keys1.length:
            return False

        ret = True
        for k in keys0:
            if self[k] != o[k]:
                ret = False
                break
            pass

        return ret

    def __ne__ (self, o):
        return not (self == o)

    def __lshift__ (self, o):
        return self.append (**{o[0] : o[1]})

    def append (self, **kwargs):
        d = {}
        for k in self:
            d[k] = self[k]
            pass

        for k, v in kwargs.items ():
            d[k] = v
            pass

        return self.__class__ (**d)

    def concat (self, o):
        d = {}
        for k in self:
            d[k] = self[k]
            pass

        for k in o:
            d[k] = o[k]
            pass

        return self.__class__ (**d)


    @property
    def isEmpty (self):
        return len (list (self)) == 0

    @property
    def items (self):
        lis = []
        for k in self:
            lis.append ((k, self[k]))
            pass

        return sleepy.collection.List (*lis)

    @property
    def keys (self):
        return sleepy.collection.List.fromIterator (iter (self))

    @property
    def length (self):
        return len (self)

    @property
    def values (self):
        return sleepy.collection.List.fromIterator (iter (self)).map (lambda x: self[x])
    
    def __setitem__ (self, key, value):
        raise AttributeError ("Map is immutable.")

    def toBuiltinMap (self):
        d = {}
        for k in self:
            d[k] = self[k]
            pass

        return d
    
    pass


class Map (MapLike):

    @staticmethod
    def fromIterator (it):
        m = Map ()
        for (k, v) in it:
            m._map[k] = v
            pass

        return m

    def __init__ (self, **kwargs):
        self._map = kwargs
        pass

    def __getitem__ (self, key):
        return self._map[key]

    def __iter__ (self):
        return self._map.iterkeys ()

    def __repr__ (self):
        return "Map(%s)" % ", ".join (self.items.map (lambda x: "%s=%s" % x))

    pass

class MMapLike (MapLike):

    def __setitem__ (self, key, value):
        raise NotImplemented ("__setitem__")

    def appendD (self, **kwargs):
        for k in kwargs:
            self[k] = kwargs[k]
            pass
        pass

    def concatD (self, o):
        for k in o:
            self[k] = o[k]
            pass
        pass
    
    pass

class MMap (MMapLike):

    @staticmethod
    def fromIterator (it):
        m = Map ()
        for (k, v) in it:
            m._map[k] = v
            pass

        return m

    def __init__ (self, **kwargs):
        self._map = copy.deepcopy (kwargs)
        pass

    def __getitem__ (self, key):
        return self._map[key]

    def __iter__ (self):
        return self._map.iterkeys ()

    def __setitem__ (self, key, value):
        self._map[key] = value
        pass

    def __repr__ (self):
        return "MMap(%s)" % ", ".join (self.items.map (lambda x: "%s=%s" % x))

    pass
