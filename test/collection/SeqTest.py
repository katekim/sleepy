import unittest
from sleepy.collection import List, Nil, Seq

class SeqTest (unittest.TestCase):

    def testArith (self):
        self.assertEquals (List (1, 3, 5, 7), Seq.arith (1, 2).take (4))
        pass

    def testGeom (self):
        self.assertEquals (List (2, 4, 8, 16, 32), Seq.geom (2, 2).take (5))
        pass

    def testSeq (self):
        
        pass

    pass
