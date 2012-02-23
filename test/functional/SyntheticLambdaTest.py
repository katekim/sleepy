import datetime, operator, unittest
import sleepy
from sleepy.extract import *

class SyntheticLambdaTest(unittest.TestCase):

    def testNoop(self):
        self.assertEquals(1, SL.fn(1)(_)(1))

    def testArithmetic(self):
        self.assertEquals(3, SL.fn(1)(_ + 2)(1))
        self.assertEquals(3, SL.fn(1)(2 + _)(1))

        self.assertEquals(-1, SL.fn(1)(_ - 2)(1))
        self.assertEquals(1,  SL.fn(1)(2 - _)(1))

        self.assertEquals(6, SL.fn(1)(_ * 2)(3))
        self.assertEquals(6, SL.fn(1)(2 * _)(3))

        self.assertEquals(3, SL.fn(1)(_ / 2)(6))
        self.assertEquals(3, SL.fn(1)(6 / _)(2))

        self.assertEquals(2, SL.fn(1)(_ % 3)(5))
        self.assertEquals(2, SL.fn(1)(5 % _)(3))

    def testComparison(self):
        self.assertTrue (SL.fn(1)(_ == 1)(1))
        self.assertTrue (SL.fn(1)(1 == _)(1))
        self.assertFalse(SL.fn(1)(_ == 1)(2))
        self.assertFalse(SL.fn(1)(1 == _)(2))

        self.assertTrue (SL.fn(1)(_ != 1)(2))
        self.assertTrue (SL.fn(1)(1 != _)(2))
        self.assertFalse(SL.fn(1)(_ != 1)(1))
        self.assertFalse(SL.fn(1)(1 != _)(1))

        self.assertTrue (SL.fn(1)(_ < 2)(1))
        self.assertFalse(SL.fn(1)(2 < _)(1))

        self.assertFalse(SL.fn(1)(_ > 2)(1))
        self.assertTrue (SL.fn(1)(2 > _)(1))

        self.assertTrue (SL.fn(1)(_ <= 2)(1))
        self.assertFalse(SL.fn(1)(2 <= _)(1))

        self.assertFalse(SL.fn(1)(_ >= 2)(1))
        self.assertTrue (SL.fn(1)(2 >= _)(1))

        self.assertFalse(SL.fn(2)(_[0] == _[1])(1, 2))
        self.assertTrue (SL.fn(2)(_[0] == _[1])('1', '1'))

    def testUDCall(self):
        lis = ML()

        def f(n):
            lis.appendD(n)

        List(1, 2, 3).foreach(_.f_(f)(_ * 2))
        self.assertEquals(List(2, 4, 6), lis)

    def testNamedVars(self):
        self.assertEquals(3, SL.fn(_.n)(_.n + 1)(2))
        self.assertEquals(3, SL.fn(_.a, _.b)(_.a + _.b)(1, 2))

    def testErrors(self):
        self.assertRaises(ValueError, SL.fn)
        self.assertRaises(ValueError, SL.fn, 0, 1)

    def testCmp(self):
        f1 = F2(_[0].cmp_(_[1]))
        self.assertTrue(f1(1, 1) == 0)
        self.assertTrue(f1(-10, 1) < 0)
        self.assertTrue(f1(5, 1) > 0)

        self.assertTrue(f1(datetime.datetime(2010, 1, 1), datetime.datetime(2010, 1, 1)) == 0)
        self.assertTrue(f1(datetime.datetime(2010, 1, 1), datetime.datetime(2011, 1, 1)) < 0)
        self.assertTrue(f1(datetime.datetime(2011, 1, 1), datetime.datetime(2010, 1, 1)) > 0)

    def testInterval(self):
        lis = Seq.arith(1, 1).takeWhile(_ <= 10).toList()

        self.assertEquals(List(4, 5, 6), lis.filter(_.cc_(4, 6)))
        self.assertEquals(List(5, 6), lis.filter(_.oc_(4, 6)))
        self.assertEquals(List(4, 5), lis.filter(_.co_(4, 6)))
        self.assertEquals(List(5), lis.filter(_.oo_(4, 6)))

    def testLogOp(self):
        lis = Seq.arith(1, 1).takeWhile(_ <= 10).toList()

        self.assertEquals(List(4, 5, 6), lis.filter(_.and_(4 <= _, _ <= 6)))
        self.assertEquals(List(1, 2, 8, 9, 10), lis.filter(_.or_(_ <= 2, 8 <= _)))
        self.assertEquals(List(1, 9, 10), lis.filter(_.xor_(2 <= _, _ <= 8)))
        self.assertEquals(List(1, 2, 3), lis.filter(_.not_(4 <= _)))

        def _True():
            result.append("T")
            return True

        def _False():
            result.append("F")
            return False

        result = []
        F0(_.and_(_.f_(_True)(), _.f_(_False)(), _.f_(_True)()))()
        self.assertEquals(["T", "F"], result)

        result = []
        F0(_.or_(_.f_(_False)(), _.f_(_True)(), _.f_(_True)()))()
        self.assertEquals(["F", "T"], result)


if __name__ == '__main__':
    unittest.main()
