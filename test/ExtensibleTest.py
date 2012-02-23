import operator, unittest
import sleepy

class TestClass1 (sleepy.Extensible):

    def __init__ (self):
        sleepy.Extensible.__init__ (self)
        pass

    pass

class TestClass2 (sleepy.Extensible):

    def __init__ (self):
        sleepy.Extensible.__init__ (self)
        pass

    pass

class ExtensibleTest (unittest.TestCase):

    def _test (self):
        obj1 = TestClass1 ()
        obj2 = TestClass2 ()
        
        TestClass1.prototype['n'] = 1

        self.assertEquals (1, obj1.n)
        self.assertRaises (AttributeError, lambda : obj2.n)

        pass

    pass


if __name__ == '__main__':
    unittest.main ()
    pass
