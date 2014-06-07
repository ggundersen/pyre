#!/usr/bin/env python
# -*- coding: utf-8 -*-

# -----------------------------------------------------------------------------
# pyre.py
# A Python implementation of regular expressions.
#
# See:
# [1] http://ezekiel.vancouver.wsu.edu/~cs317/archive/projects/grep/grep.pdf
# [2] http://swtch.com/~rsc/regexp/regexp1.html
# [3] http://csis.pace.edu/~wolf/CS122/infix-postfix.htm
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
            '$': 4,
            '(': 0,
            ')': 0
        }

    def compile(self, re):
        post = self.in2post(re)
        print(post)

    # Calculates operator precedence. See [4]
    def prec(self, char):
        return self.operators[char]

    # "...postﬁx notation [is] nice because parentheses are unneeded since [it
    # does] not have the operator-operand ambiguity inherent to inﬁx 
    # expressions."[1]
    #
    # We will use the "&" symbol as an explicit concatentation operator.
    # Ken Thompson originally used the "."[2] but we want to use the dot as a
    # wild card. 
    #
    # The algorithm used is from [3].
    def in2post(self, in_str):
        post_str = ''
        stack = list()

        for char in in_str:
            print 'char: ' + char
            if char in self.operators:
                print '\t' + char + ' is in the list of operators'
                if not stack:
                    print '\t\t' + 'stack empty, placing ' + char + ' onto stack'
                    stack.append(char)
                # If `char` has a higher precedence than the top of the stack:
                elif self.prec(char) > self.prec(stack[-1]):
                    print '\t\t' + char + ' has higher precedence, placed onto stack'
                    stack.append(char)
                # If `char` has a lower precedence:
                else:
                    # If we see an open paren, do not pop operators off stack.
                    if char is '(':
                        # Place open paren on stack as a marker
                        print '\t\topen paren found, placing on stack'
                        stack.append(char)
                    elif char is ')':
                        print '\t\tclose paren found, pop stack until find open paren'
                        while stack and stack[-1] is not '(':
                            post_str += stack.pop()
                    else:
                        while stack and self.prec(char) <= self.prec(stack[-1]):
                            print '\t\t' + char + ' has lower or equal precedence than ' + stack[-1] + ', pop top of stack'
                            post_str += stack.pop()
                            print '\t\t\t' + str(stack)
                            print '\t\t\t' + post_str
                        stack.append(char)
            else:
                print '\t' + char + ' is literal'
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
