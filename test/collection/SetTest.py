import unittest
from sleepy.collection import Set

class SetTest (unittest.TestCase):

    def testIn (self):
        self.assertTrue (1 in Set (1, 2, 3))
        self.assertTrue (4 not in Set (1, 2, 3))
        self.assertFalse (4 in Set (1, 2, 3))
        pass

    def testIsDisjoint (self):
        self.assertTrue (Set ().isDisjoint (Set ()))
        self.assertTrue (Set (1, 2).isDisjoint (Set (3, 4)))
        self.assertFalse (Set (1, 2).isDisjoint (Set (2, 3)))
        pass

    def testLength (self):
        self.assertEqual (0, Set ().length ())
        self.assertEqual (3, Set (1, 2, 3).length ())
        self.assertEqual (2, Set (1, 1, 2).length ())
        pass

    pass


if __name__ == '__main__':
    unittest.main ()
    pass
