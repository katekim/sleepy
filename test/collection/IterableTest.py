import operator, sleepy, unittest
from sleepy.collection import List, Nil
from sleepy.extract import *

class IterableTest (unittest.TestCase):

    def testCount (self):
        pass

    def testDrop (self):
        self.assertEquals (Nil, Nil.drop (3))
        self.assertEquals (Nil, List (1, 2, 3).drop (3))
        self.assertEquals (List (4, 5), List (1, 2, 3, 4, 5).drop (3))
        self.assertEquals (List (1, 2, 3), List (1, 2, 3).drop (0))
        pass

    def testDropWhile (self):
        self.assertEquals (List (3, 4, 5), List (1, 2, 3, 4, 5).dropWhile (_ <= 2))
        self.assertEquals (List (1, 2, 3, 4, 5), List (1, 2, 3, 4, 5).dropWhile (_ >= 2))
        self.assertEquals (Nil, List (1, 2, 3, 4, 5).dropWhile (_ >= 0))
        pass

    def testExists (self):
        self.assertEquals (False, Nil.exists (lambda x: x == 0))
        self.assertEquals (True, List (1, 2, 3).exists (lambda x: x % 2 == 0))
        self.assertEquals (True, List (1, 2, 3, 4, 5).exists (_ % 2 == 0))
        self.assertEquals (False, List (1, 2, 3, 4, 5).exists (_ > 10))
        pass

    def testFilter (self):
        self.assertEquals (Nil, Nil.filter (lambda x: True))
        self.assertEquals (List (2, 4), List (1, 2, 3, 4, 5).filter (_ % 2 == 0))
        self.assertEquals (Nil, List (1, 2, 3, 4, 5).filter (_ > 10))
        self.assertEquals (List, List (1, 2, 3, 4, 5).filter (lambda x: x > 10).__class__)
        pass

    def testFold (self):
        self.assertEquals (1, Nil.fold (1, operator.add))
        self.assertEquals (3, List (2).fold (1, operator.add))
        self.assertEquals (6, List (2, 3).fold (1, _[0] + _[1]))
        pass

    def testForall (self):
        self.assertEquals (True, Nil.forall (lambda x: x == 0))
        self.assertEquals (False, List (1, 2, 3).forall (_ % 2 == 0))
        self.assertEquals (True, List (2, 4).forall (_ % 2 == 0))
        pass

    def testForeach (self):

        class Trace:

            def __init__ (self):
                self._args = []
                pass

            def __call__ (self, args):
                self._args.append (args)
                pass

            pass

        tr1 = Trace ()
        Nil.foreach (tr1)
        self.assertEquals ([], tr1._args)

        tr2 = Trace ()
        List (1, 2, 3).foreach (tr2)
        self.assertEquals ([1, 2, 3], tr2._args)

        pass
    
    def testMap (self):
        self.assertEquals (Nil, Nil.map (lambda x: x))
        self.assertEquals (List (2, 4, 6), List (1, 2, 3).map (_ * 2))
        pass

    def testMinMax (self):
        self.assertRaises (ValueError, lambda : List ().min)
        self.assertEquals (1, List (1).min)
        self.assertEquals (1, List (1, 2, 3).min)
        self.assertEquals (1, List (1, 2, 3, 1).min)

        self.assertRaises (ValueError, lambda : List ().max)
        self.assertEquals (1, List (1).max)
        self.assertEquals (3, List (1, 2, 3).max)
        self.assertEquals (3, List (2, 1, 2, 3).max)
        pass

    def testProduct (self):
        self.assertEquals (1, List ().product)
        self.assertEquals (1, List (1).product)
        self.assertEquals (24, List (2, 3, 4).product)
        pass
    
    def testReduce (self):
        self.assertRaises (TypeError, List ().reduce, operator.add)
        self.assertEquals (1, List (1).reduce (operator.add))
        self.assertEquals (10, List (1, 2, 3, 4).reduce (_[0] + _[1]))
        pass

    def testSum (self):
        self.assertEquals (0, List ().sum)
        self.assertEquals (1, List (1).sum)
        self.assertEquals (6, List (1, 2, 3).sum)
        pass

    def testTake (self):
        self.assertEquals (List (1, 2, 3), List (1, 2, 3, 4, 5).take (3))
        self.assertEquals (List (1, 2), List (1, 2).take (3))
        self.assertEquals (Nil, Nil.take (3))
        pass

    def testTakeWhile (self):
        self.assertEquals (List (1, 2, 3), List (1, 2, 3, 4, 5).takeWhile (_ <= 3))
        self.assertEquals (Nil, List (1, 2, 3, 4, 5).takeWhile (_ >= 3))
        pass

    def testUnique (self):
        self.assertEquals (Nil, Nil.unique)
        self.assertEquals (L (1), L (1).unique)
        self.assertEquals (L (1, 2), L (1, 1, 2).unique)
        self.assertEquals (L (1), L (1, 1, 1).unique)
        pass

    def testZip (self):
        self.assertEquals (List ((1, 4), (2, 5), (3, 6)),
                           List (1, 2, 3).zip (List (4, 5, 6)))

        self.assertEquals (List ((1, 4), (2, 5)),
                           List (1, 2).zip (List (4, 5, 6)))

        self.assertEquals (List ((1, 4), (2, 5)),
                           List (1, 2, 3).zip (List (4, 5)))

        self.assertEquals (List ((1, 4), (2, 5)),
                           List (1, 2, 3).zip (List (4, 5)))

        self.assertEquals (List ((1, 4, 7), (2, 5, 8), (3, 6, 9)),
                           List (1, 2, 3).zip (List (4, 5, 6), List (7, 8, 9)))
        pass

    def testZipFilled (self):
        self.assertEquals (List ((1, 4), (2, 5), (None, 6)),
                           List (1, 2).zipFilled (List (4, 5, 6)))

        self.assertEquals (List ((1, 4), (2, 5), (-1, 6)),
                           List (1, 2).zipFilled (List (4, 5, 6), fill = -1))

        self.assertEquals (List ((1, 4), (2, 5), (3, -1)),
                           List (1, 2, 3).zipFilled (List (4, 5), fill = -1))
        pass

    pass


if __name__ == '__main__':
    unittest.main ()
    pass
