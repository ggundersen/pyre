import unittest

from pyre import Pyre


class TestIn2Post(unittest.TestCase):

    def setUp(self):
        self.re = Pyre()

    def test_postfix(self):
        post_str = self.re.in2post('a+b')
        self.assertEqual(post_str, 'ab+')

    def test_higher_precedence(self):
        post_str = self.re.in2post('a+b*c')
        self.assertEqual(post_str, 'abc*+')

    def test_lower_precedence(self):
        post_str = self.re.in2post('a*b+c')
        self.assertEqual(post_str, 'ab*c+')
        

if __name__ == '__main__':
    unittest.main()
