import unittest

from pyre import Pyre


class TestIn2Post(unittest.TestCase):

    def setUp(self):
        self.fn = Pyre().in2post

    def test_postfix(self):
        post = self.fn('a+b')
        self.assertEqual(post, 'ab+')

    def test_higher_precedence(self):
        post = self.fn('a+b*c')
        self.assertEqual(post, 'abc*+')

    def test_lower_precedence(self):
        post = self.fn('a*b+c')
        self.assertEqual(post, 'ab*c+')

    def test_equal_precedence(self):
        post = self.fn('a+b-c')
        self.assertEqual(post, 'ab+c-')
        post = self.fn('a-b+c')
        self.assertEqual(post, 'ab-c+')

    def test_removing_parens(self):
        post = self.fn('(a+b)')
        self.assertEqual(post, 'ab+')

    def test_parens_precedence(self):
        post = self.fn('(a+b)*c')
        self.assertEqual(post, 'ab+c*')

    def test_nested_parens(self):
        post = self.fn('(a+(b-c))*d')
        self.assertEqual(post, 'abc-+d*')
        

if __name__ == '__main__':
    unittest.main()
