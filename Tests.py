import unittest
import requests


class TestSum(unittest.TestCase):

    def test_not_empty_students(self):
        r = requests.get("http://localhost:5000/getStudents").json()
        self.assertTrue(len(r["students"]) > 0, "Should be not empty database")

    def test_add_student(self):
        r = requests.delete("http://localhost:5000/deleteAll")
        self.assertTrue(r.text == "Deleted", "Should be deleted")


if __name__ == '__main__':
    unittest.main()