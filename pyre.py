#!/usr/bin/env python
# -*- coding: utf-8 -*-

# -----------------------------------------------------------------------------
# pyre.py
# A Python implementation of regular expressions.
#
# See:
# [1] http://ezekiel.vancouver.wsu.edu/~cs317/archive/projects/grep/grep.pdf
# [2] http://swtch.com/~rsc/regexp/regexp1.html
# [3] http://scriptasylum.com/tutorials/infix_postfix/algorithms/infix-postfix/
# [4] http://stackoverflow.com/q/60208/1830334
# -----------------------------------------------------------------------------


import sys


class Pyre:

    def __init__(self):
        self.operators = {
            '|': 9,
            '*': 8,
            '+': 7,
            '-': 7,
            '?': 6,
            '^': 5,
            '$': 4
        }


    def compile(self, re):
        post = self.re2post(re)
        print(post)

    
    # Calculates operator precedence. See [4]
    def prec(self, char):
        return self.operators[char].get(char, 0)


    # "...postﬁx notation [is] nice because parentheses are unneeded
    # since [it does] not have the operator-operand ambiguity inherent to inﬁx
    # expressions."[1]
    #
    # The idea is to eliminate parenthesis, for example:
    # ((a|b)*aba*)*(a|b)(a|b)
    # will be converted to
    # ab|*a&b&a*&*ab|&ab|&
    #
    # We will use the "&" symbol as an explicit concatentation operator.
    # Ken Thompson originally used the "."[2] but we want to use the dot as a
    # wild card. 
    #
    # The algorithm used is from [3].
    def re2post(self, in_str):
        post_str = ''
        stack = list()

        for char in in_str:
            if char in self.operators:
                if not stack:
                    stack.append(char)
                # If `char` has a higher precedence than the top of the stack:
                elif self.prec(char) < self.prec(stack[-1]):
                    stack.append(char)
                # If `char` has a lower precedence:
                else:
                    post_str += stack.pop()
            else:
                post_str += char

        while stack:
            post_str += stack.pop()

        return post_str


    # "We will convert a postﬁx regular expression into an NFA using a stack,
    # where each element on the stack is an NFA."
    def post2nfa(post):
        pass


    def match(self, str):
        pass


if __name__ == '__main__':
    pyre = Pyre()
    pyre.compile(sys.argv[1])
    pyre.match('aab')
