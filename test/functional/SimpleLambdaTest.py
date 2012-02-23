import operator, unittest
import sleepy
from sleepy.extract import *

class SimpleLambdaTest (unittest.TestCase):

    # def testNoop (self):
    #     self.assertEquals (1, _ (1))
    #     pass

    # def testArithmetic (self):
    #     self.assertEquals (3, (_ + 2) (1))
    #     self.assertEquals (3, (2 + _) (1))

    #     self.assertEquals (-1, (_ - 2) (1))
    #     self.assertEquals (1, (2 - _) (1))

    #     self.assertEquals (6, (_ * 2) (3))
    #     self.assertEquals (6, (2 * _) (3))

    #     self.assertEquals (3, (_ / 2) (6))
    #     self.assertEquals (3, (6 / _) (2))

    #     self.assertEquals (2, (_ % 3) (5))
    #     self.assertEquals (2, (5 % _) (3))
    #     pass

    # def testComparison (self):
    #     self.assertEquals (True, (_ == 1) (1))
    #     self.assertEquals (True, (1 == _) (1))
    #     self.assertEquals (False, (_ == 1) (2))
    #     self.assertEquals (False, (1 == _) (2))

    #     self.assertEquals (True, (_ != 1) (2))
    #     self.assertEquals (True, (1 != _) (2))
    #     self.assertEquals (False, (_ != 1) (1))
    #     self.assertEquals (False, (1 != _) (1))

    #     self.assertEquals (True, (_ < 2) (1))
    #     self.assertEquals (False, (2 < _) (1))

    #     self.assertEquals (False, (_ > 2) (1))
    #     self.assertEquals (True, (2 > _) (1))

    #     self.assertEquals (True, (_ <= 2) (1))
    #     self.assertEquals (False, (2 <= _) (1))

    #     self.assertEquals (False, (_ >= 2) (1))
    #     self.assertEquals (True, (2 >= _) (1))

    #     self.assertEquals (False, (_[0] == _[1]) (1, 2))
    #     self.assertEquals (True, (_[0] == _[1]) ('1', '1'))

    #     self.assertEquals ([1, 2, 3], List (3, 1, 2).sort (_[0] - _[1]).toBuiltinList ())
    #     pass

    # def testBinary (self):
    #     self.assertEquals (5, (_[0] + _[1]) ((2, 3)))
    #     self.assertEquals (6, (_[0] + (_[1] + 1)) ((2, 3)))
    #     self.assertEquals (7, ((_[0] + 1) + (_[1] + 1)) ((2, 3)))
    #     self.assertEquals (9, (_[0] + _[1] + _[2]) ((2, 3, 4)))
    #     pass

    # def testCall (self):

    #     class Trace:

    #         def __init__ (self):
    #             self._args = None
    #             self._kwargs = None
    #             pass

    #         def f (self, *args, **kwargs):
    #             self._args = args
    #             self._kwargs = kwargs
    #             pass

    #         pass

    #     tr1 = Trace ()
    #     (_.f ()) (tr1)
    #     self.assertEquals ((), tr1._args)
    #     self.assertEquals ({}, tr1._kwargs)

    #     tr2 = Trace ()
    #     (_.f (1, 2, 3, a = 'one', b = 'two')) (tr2)
    #     self.assertEquals ((1, 2, 3), tr2._args)
    #     self.assertEquals ('one', tr2._kwargs['a'])
    #     self.assertEquals ('two', tr2._kwargs['b'])
    #     pass

    pass


if __name__ == '__main__':
    unittest.main ()
    pass
