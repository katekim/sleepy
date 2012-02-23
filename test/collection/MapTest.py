import operator, unittest
from sleepy.collection import Nil, List, Map, MMap

class MapTest (unittest.TestCase):

    def testCtor (self):
        self.assertEquals (Map (), Map ())
        self.assertEquals (Map (one = 1), Map (one = 1))
        self.assertEquals (Map (one = 1, two = 2), Map (two = 2, one = 1))
        pass

    def testAppend (self):
        self.assertEquals (Map (one = 1, two = 2), Map (one = 1).append (two = 2))
        self.assertEquals (Map (one = 1, two = 2), (Map (one = 1) << ("two", 2)))
        self.assertEquals (Map (one = 2), Map (one = 1).append (one = 2))
        pass

    def testConcat (self):
        self.assertEquals (Map (), Map () + Map ())
        self.assertEquals (Map (one = 1, two = 2), Map (two = 2) + Map (one = 1))
        self.assertEquals (Map (one = 2), Map (one = 1) + Map (one = 2))
        self.assertEquals (Map (one = 1, two = 2, three = 3), Map (two = 2) + Map (one = 1, three = 3))
        pass

    def testEq (self):
        self.assertTrue (Map () == Map ())
        self.assertTrue (Map (one = 1) == Map (one = 1))
        self.assertFalse (Map (one = 1) == Map (one = 2))
        self.assertTrue (Map (one = 1) != Map (one = 2))
        self.assertTrue (Map (one = 1) != Map (one = 1, two = 2))
        self.assertTrue (Map (two = 2, one = 1) == Map (one = 1, two = 2))
        pass

    def testFromDict (self):
        self.assertEquals (Map (), Map.fromDict ({}))
        self.assertEquals (Map (**{'a-b' : 1}), Map.fromDict ({'a-b' : 1}))
        pass

    def testFromIterator (self):
        self.assertEquals (Map (one = 1, two = 2), Map.fromIterator (List (("one", 1), ("two", 2))))
        self.assertEquals (Map (), Map.fromIterator (List ()))
        pass

    def testIsEmpty (self):
        self.assertTrue (Map ().isEmpty)
        self.assertFalse (Map (one = 1, two = 2).isEmpty)
        pass

    def testKeys (self):
        self.assertEquals (Nil, Map ().keys)
        self.assertEquals (List ('one', 'two'), Map (one = 1, two = 2).keys.toList ().sort ())
        pass

    def testLength (self):
        self.assertEquals (0, Map ().length)
        self.assertEquals (2, Map (one = 1, two = 2).length)
        pass

    def testValues (self):
        self.assertEquals (Nil, Map ().values)
        self.assertEquals (List (1, 2), Map (one = 1, two = 2).values.toList ().sort ())
        pass

    def testItems (self):
        self.assertEquals (Nil, Map ().items)
        self.assertEquals (List (('one', 1), ('two', 2)), Map (one = 1, two = 2).items.toList ().sort ())
        pass

    def testImmutable (self):
        m = Map (one = 1)
        self.assertRaises (AttributeError, lambda : m.__setitem__ ("one", 2))
        pass

    def testMerge (self):
        pass
    
    pass


class MMapTest (unittest.TestCase):

    def testAppendD (self):
        m = MMap (one = 1)
        m.appendD (two = 2)
        self.assertEquals (MMap (one = 1, two = 2), m)

        m.appendD (one = 3)
        self.assertEquals (MMap (one = 3, two = 2), m)
        pass

    def testAssign (self):
        m = MMap (one = 1)
        m["one"] = 2
        self.assertEquals (2, m["one"])
        pass

    def testConcatD (self):
        m = MMap (one = 1)
        m.concatD (Map (two = 2))
        self.assertEquals (Map (one = 1, two = 2), m)
        pass
    
    pass


if __name__ == '__main__':
    sys.exit (SignalFinder ().main (sys.argv[1:]))
    pass

