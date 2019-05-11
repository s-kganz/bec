from bec import one
import unittest

class Test_TestOne(unittest.TestCase):
    def test_one(self):
        result = one()
        self.assertEqual(result, 1)

if __name__ == "__main__":
    unittest.main()