import unittest
from app import some_method_for_test


class TestSum(unittest.TestCase):

    def test1(self):
        self.assertTrue(some_method_for_test(1) == 2, "Should be not empty database")

    def test2(self):
        self.assertTrue(some_method_for_test(2) == 4, "Should be not empty database")


if __name__ == '__main__':
    unittest.main()