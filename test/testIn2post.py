#!/usr/bin/env python
# -*- coding: utf-8 -*-

# -----------------------------------------------------------------------------
# testIn2post.py
#
# Tests Pyre's `__in2post()` function, which converts an infix expression to a
# postfix expression. Importantly, the function also converts implicit
# concatenation to explicit concatenation.
# -----------------------------------------------------------------------------


import sys
sys.path.append('~/pyre')
import unittest

#from pyre import *
from pyre import pyre


class TestIn2post(unittest.TestCase):

    def setUp(self):
        self.Pyre = pyre.Pyre
        self.use_debug = False

    def test_postfix(self):
        p = self.Pyre('', self.use_debug)
        print( p._Pyre__in2post('a+b') )

    '''def test_higher_precedence(self):
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
        self.assertEqual(post, 'abc-+d*')'''
