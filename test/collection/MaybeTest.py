import operator, sleepy, unittest
from sleepy.collection import List, Just, Nothing
from sleepy.extract import *

class MaybeTest (unittest.TestCase):

    def testGet (self):
        self.assertEquals (1, Just (1).get ())
        self.assertRaises (ValueError, Nothing.get)
        pass

    def testGetOrElse (self):
        self.assertEquals (1, Just (1).getOrElse (2))
        self.assertEquals (2, Nothing.getOrElse (2))
        pass

    def testIsNothing (self):
        self.assertFalse (Just (1).isEmpty)
        self.assertTrue (Nil.isEmpty)
        self.assertTrue (Just (1).nonEmpty)
        self.assertFalse (Nil.nonEmpty)
        pass

    def testIter (self):
        self.assertEquals (List (1), List.fromIterator (Just (1)))
        self.assertEquals (Nil, List.fromIterator (Nothing))
        self.assertEquals (List (1, 2), List (Just (1), Nothing, Just (2), Nothing).flatten ())
        pass

    pass
