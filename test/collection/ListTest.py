import unittest
from sleepy.collection import List, MList, Nil

class ListTest (unittest.TestCase):

    def testAccess (self):
        self.assertEquals (1, List (0, 1, 2)[1])

        lis = MList (0, 1, 2)
        lis[0] = 3
        self.assertEquals (3, lis[0])
        pass

    def testAppend (self):
        self.assertEquals (List (1), Nil.append (1))
        self.assertEquals (List (1, 2, 3, 4), List (1, 2).append (3, 4))
        self.assertEquals (List (1, 2), List (1, 2).append ())

        self.assertEquals (List (1, 2, 3), List (1, 2) << 3)
        pass

    def testAppendD (self):
        lis = MList ()

        lis <<= 1
        self.assertEquals (List (1), lis)

        lis.appendD (2, 3, 4)
        self.assertEquals (List (1, 2, 3, 4), lis)

        lis.appendD ()
        self.assertEquals (List (1, 2, 3, 4), lis)
        pass

    def testConcat (self):
        self.assertEquals (List (1, 2, 3), List (1).concat (List (2, 3)))
        self.assertEquals (List (1, 2, 3), List (1) + List (2, 3))
        pass

    def testContains (self):
        self.assertFalse (Nil.contains (1))
        self.assertTrue (List (1, 2, 3).contains (2))
        self.assertFalse (List (1, 2, 3).contains (4))
        pass

    def testEndsWith (self):
        self.assertTrue (List (1, 2, 3).endsWith (List (2, 3)))
        self.assertFalse (List (1, 2, 3).endsWith (List (1, 2)))
        self.assertFalse (Nil.endsWith (List (1, 2)))
        self.assertTrue (Nil.endsWith (Nil))
        pass

    def testFlatten (self):
        self.assertEquals (List (1, 2, 3), List (List (1), List (2, 3)).flatten ())
        self.assertEquals (List (1, 2, 3), List (List (1), Nil, List (2, 3)).flatten ())
        self.assertEquals (List (1, 2, List (3)), List (List (1), List (2, List (3))).flatten ())
        pass

    def testPrepend (self):
        self.assertEquals (List (1), Nil.prepend (1))
        self.assertEquals (List (1, 2, 3), List (2, 3).prepend (1))
        self.assertEquals (List (1, 2, 3), 1 >> List (2, 3))
        pass

    def testInit (self):
        self.assertEquals (Nil, List ())
        self.assertEquals (List (1), List (1))
        self.assertEquals (List (1, "two", 3.0), List (1, "two", 3.0))
        pass

    def testFromIterator (self):
        self.assertEquals (List (), List.fromIterator ([]))
        self.assertEquals (List (1, 2, 3), List.fromIterator ((1, 2, 3)))
        self.assertEquals (List (0, 1, 2), List.fromIterator (xrange (3)))

        def gen ():
            for x in range (3):
                yield x
                pass
            pass

        self.assertEquals (List (0, 1, 2), List.fromIterator (gen ()))
        pass

    def testHead (self):
        self.assertRaises (IndexError, lambda : List ().head)
        self.assertEquals (1, List (1, 2, 3).head)
        pass

    def testIndex (self):
        self.assertRaises (ValueError, Nil.index, "one")
        self.assertEquals (0, List ("one", "two").index ("one"))
        pass

    def testIsEmpty (self):
        self.assertTrue (List ().isEmpty)
        self.assertFalse (List (1, 2, 3).isEmpty)

        self.assertFalse (List ().nonEmpty)
        self.assertTrue (List (1, 2).nonEmpty)
        pass

    def testLast (self):
        self.assertRaises (IndexError, lambda : List ().last)
        self.assertEquals (3, List (1, 2, 3).last)
        pass

    def testLength (self):
        self.assertEquals (0, List ().length)
        self.assertEquals (3, List (1, 2, 3).length)
        self.assertEquals (3, len (List (1, 2, 3)))
        pass

    def testReverse (self):
        self.assertEquals (Nil, Nil.reverse ())
        self.assertEquals (List (1), List (1).reverse ())
        self.assertEquals (List (3, 2, 1), List (1, 2, 3).reverse ())
        pass

    def testReverseD (self):
        lis = MList (1, 2, 3)
        lis.reverseD ()
        self.assertEquals (List (3, 2, 1), lis)
        pass

    def testSlice (self):
        self.assertEquals (List (1, 2), List (0, 1, 2, 3)[1:3])
        self.assertEquals (Nil, List (0, 1, 2, 3)[5:7])
        self.assertEquals (Nil, List (0, 1, 2, 3)[3:1])
        pass

    def testStartsWith (self):
        self.assertTrue (List (1, 2, 3).startsWith (List (1, 2)))
        self.assertTrue (Nil.startsWith (Nil))
        self.assertFalse (List (1, 2, 3).startsWith (List (2, 3)))
        self.assertFalse (List (1).startsWith (List (1, 2)))
        pass

    def testTail (self):
        self.assertRaises (IndexError, lambda : List ().tail)
        self.assertEquals (List (2, 3), List (1, 2, 3).tail)
        pass

    pass


if __name__ == '__main__':
    unittest.main ()
    pass
