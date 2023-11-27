import unittest

from modules.Tweeter import Tweeter


class MyTestCase(unittest.TestCase):
    def test_case1(self):
        self.assertTrue(1 == 1)

if __name__ == '__main__':
    unittest.main()
