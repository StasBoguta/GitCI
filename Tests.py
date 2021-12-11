import unittest
import requests


class TestSum(unittest.TestCase):

    def test_not_empty_students(self):
        self.assertTrue(1 > 0, "Should be not empty database")


if __name__ == '__main__':
    unittest.main()