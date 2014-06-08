import unittest

from pyre import Pyre


class TestIn2Post(unittest.TestCase):

    def setUp(self):
        self.re = Pyre()

    def test_x(self):
        post_str = self.re.in2post('abc')
        self.assertEqual(post_str, 'abc')
        

if __name__ == '__main__':
    unittest.main()
