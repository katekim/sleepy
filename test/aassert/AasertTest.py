import datetime, unittest, sleepy
from sleepy.extract import *

class AAssertTest (unittest.TestCase):

    def testAnd (self):

        @aa (aa.var ("n").and_ (aa.ofType (int),
                                aa.ge (0)))
        def f1 (n): return n * 2

        self.assertEquals (6, f1 (3))
        self.assertRaises (ValueError, f1, "3")
        self.assertRaises (ValueError, f1, 3.0)
        pass

    def testCallable (self):

        class FuncObj:

            def __call__ (self):
                return "FuncObj"

            pass

        @aa (aa.var ("fn").callable ())
        def f1 (fn): return fn ()

        self.assertEquals (1, f1 (lambda : 1))
        self.assertEquals ("FuncObj", f1 (FuncObj ()))
        self.assertRaises (ValueError, f1, 0)
        pass

    def testCmp (self):

        @aa (aa.var ("n").ge (0))
        def f1 (n): return n * 2

        self.assertEquals (6, f1 (3))
        self.assertEquals (0, f1 (0))
        self.assertRaises (ValueError, f1, -2)


        @aa (aa.var ("n").gt (0))
        def f2 (n): return n * 2

        self.assertEquals (6, f2 (3))
        self.assertRaises (ValueError, f2, 0)
        self.assertRaises (ValueError, f2, -2)


        @aa (aa.var ("n").le (0))
        def f3 (n): return n * 2

        self.assertEquals (-6, f3 (-3))
        self.assertEquals (0, f3 (0))
        self.assertRaises (ValueError, f3, 2)


        @aa (aa.var ("n").lt (0))
        def f4 (n): return n * 2

        self.assertEquals (-6, f4 (-3))
        self.assertRaises (ValueError, f4, 0)
        self.assertRaises (ValueError, f4, 2)


        @aa (aa.var ("n").eq (3))
        def f5 (n): return n * 2

        self.assertEquals (6, f5 (3))
        self.assertRaises (ValueError, f5, 4)
        self.assertRaises (ValueError, f5, 5)
        pass

    def testCond (self):

        @aa (aa.var ("n").cond (lambda x: x == 1, "test"))
        def f1 (n): return n * 2

        self.assertEquals (2, f1 (1))
        self.assertRaises (ValueError, f1, 2)


        @aa (aa.var ("n").cond (_ == 1, "test"))
        def f2 (n): return n * 2

        self.assertEquals (2, f2 (1))
        self.assertRaises (ValueError, f2, 2)
        pass

    def testInterval (self):

        @aa (aa.var ("n").cc (0, 10))
        def f1 (n): return n * 2

        self.assertEquals (6, f1 (3))
        self.assertEquals (0, f1 (0))
        self.assertEquals (20, f1 (10))
        self.assertRaises (ValueError, f1, -1)
        self.assertRaises (ValueError, f1, 11)


        @aa (aa.var ("n").co (0, 10))
        def f2 (n): return n * 2

        self.assertEquals (6, f2 (3))
        self.assertEquals (0, f2 (0))
        self.assertRaises (ValueError, f2, 10)


        @aa (aa.var ("n").oc (0, 10))
        def f3 (n): return n * 2

        self.assertEquals (6, f3 (3))
        self.assertRaises (ValueError, f3, 0)
        self.assertEquals (20, f3 (10))


        @aa (aa.var ("n").oo (0, 10))
        def f4 (n): return n * 2

        self.assertEquals (6, f4 (3))
        self.assertRaises (ValueError, f4, 0)
        self.assertRaises (ValueError, f4, 10)
        pass

    def testIterable (self):

        @aa (aa.var ("lis").iterable ())
        def f1 (lis): return sum (lis)

        self.assertEquals (6, f1 ([1, 2, 3]))
        self.assertEquals (6, f1 (List (1, 2, 3)))
        self.assertRaises (ValueError, f1, 0)
        pass

    def testMultipleArgs (self):

        @aa (aa.var ("a").ofType (int),
             aa.var ("b").ofType (int))
        def f1 (a, b): return a + b

        self.assertEquals (3, f1 (1, 2))
        self.assertRaises (ValueError, f1, 1L, 2)
        self.assertRaises (ValueError, f1, 1, 2L)
        pass

    def testNot (self):

        @aa (aa.var ("n").not_ (aa.eq (3)))
        def f1 (n): return n * 2

        self.assertEquals (0, f1 (0))
        self.assertRaises (ValueError, f1, 3)
        pass

    def testOfInstance (self):

        class Base: pass
        class Derived (Base): pass

        @aa (aa.var ("obj").ofInstance (Base))
        def f1 (obj): return True

        self.assertTrue (f1 (Base ()))
        self.assertTrue (f1 (Derived ()))
        self.assertRaises (ValueError, f1, 0)
        pass

    def testOfType (self):

        @aa (aa.var ("n").ofType (int))
        def f1 (n): return n * 2

        self.assertEquals (6, f1 (3))
        self.assertRaises (ValueError, f1, 3.0)
        self.assertRaises (ValueError, f1, "3")


        @aa (aa.var ("t").ofType (datetime.datetime))
        def f1 (t): return t

        self.assertEquals (datetime.datetime (2011, 1, 1), f1 (datetime.datetime (2011, 1, 1)))
        self.assertRaises (ValueError, f1, 1)
        pass

    def testOr (self):

        @aa (aa.var ("n").or_ (aa.ofType (int),
                               aa.ofType (long)))
        def f1 (n): return n * 2

        self.assertEquals (6, f1 (3))
        self.assertEquals (6, f1 (3L))
        self.assertRaises (ValueError, f1, "3")
        pass

    def testSequential (self):

        @aa (aa.var ("lis").sequential ())
        def f1 (lis): return sum (lis)

        def gen ():
            for i in range (10):
                yield i
                pass
            pass

        self.assertEquals (6, f1 ([1, 2, 3]))
        self.assertRaises (ValueError, f1, 0)
        self.assertRaises (ValueError, f1, gen ())


        @aa (aa.var ("lis").sequential ().nonEmpty ())
        def f1 (lis): return sum (lis)

        self.assertEquals (6, f1 (L (1, 2, 3)))
        self.assertRaises (ValueError, f1, Nil)


        @aa (aa.var ("lis").sequential ().length (aa.ge (3)))
        def f2 (lis): return sum (lis)

        self.assertEquals (6, f2 (L (1, 2, 3)))
        self.assertRaises (ValueError, f2, L (1, 2))


        @aa (aa.var ("lis").sequential ().forall (aa.ge (0)))
        def f3 (lis): return sum (lis)

        self.assertEquals (6, f3 (L (1, 2, 3)))
        self.assertRaises (ValueError, f3, L (1, 2, -1))
        pass

    def testTuple (self):

        @aa (aa.var ("t").tuple ())
        def f1 (t): return True

        self.assertTrue (f1 ((1, 2, 3)))
        self.assertRaises (ValueError, f1, [1, 2, 3])


        @aa (aa.var ("t").tuple ().length (aa.eq (2)))
        def f2 (t): return True

        self.assertTrue (f2 ((1, 2)))
        self.assertRaises (ValueError, f2, [1])
        self.assertRaises (ValueError, f2, [1, 2, 3])


        @aa (aa.var ("t").tuple ().length (aa.eq (2)) \
                                  .elem (0, aa.ofType (str)) \
                                  .elem (1, aa.ofType (int)))
        def f3 (t): return True

        self.assertTrue (f3 (("1", 2)))
        self.assertRaises (ValueError, f3, (1, 2))
        self.assertRaises (ValueError, f3, ("1", 2.0))
        pass

    pass


if __name__ == '__main__':
    unittest.main ()
    pass
