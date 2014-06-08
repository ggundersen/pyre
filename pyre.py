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
from enum import Enum


class Control(Enum):
    split = 256
    match = 257


class NfaState:

    def __init__(self, control, out1, last_list, out2=None):
        self.control = control
        self.out1 = out1
        self.out2 = out2
        self.last_list = last_list


class NfaFrag:

    def __init__(self, start, out_list):
        self.start = start
        self.out_list = out_list


class Pyre:

    def __init__(self, debug=False):
        self.debug = debug
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

    def debug_print(self, msg):
        if (self.debug):
            print(msg)

    def compile(self, re):
        post = self.in2post(re)
        self.post2nfa(post)

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

    # TODO: Should convert implicit concatentation, e.g. AB, into explicit concatentation, e.g. A&B 
    def in2post(self, in_str):

        self.debug_print('IN2POST ---------------------------------')

        post = ''
        stack = list()

        for char in in_str:
            self.debug_print('char: ' + char)
            if char in self.operators:
                self.debug_print('\t' + char + ' is in the list of operators')
                if not stack:
                    self.debug_print('\t\t' + 'stack empty, placing ' + char + ' onto stack')
                    stack.append(char)
                # If `char` has a higher precedence than the top of the stack:
                elif self.prec(char) > self.prec(stack[-1]):
                    self.debug_print('\t\t' + char + ' has higher precedence, placed onto stack')
                    stack.append(char)
                # If `char` has a lower precedence:
                else:
                    # If we see an open paren, do not pop operators off stack.
                    if char is '(':
                        # Place open paren on stack as a marker
                        self.debug_print('\t\topen paren found, placing on stack')
                        stack.append(char)
                    elif char is ')':
                        # TODO: What if there is no open paren?
                        self.debug_print('\t\tclose paren found, pop stack until find open paren')
                        while stack and stack[-1] is not '(':
                            post += stack.pop()
                        # Remove open paren
                        stack.pop()
                    else:
                        while stack and self.prec(char) <= self.prec(stack[-1]):
                            self.debug_print('\t\t' + char + ' has lower or equal precedence than ' + stack[-1] + ', pop top of stack')
                            post += stack.pop()
                            self.debug_print('\t\t\t' + str(stack))
                            self.debug_print('\t\t\t' + post)
                        stack.append(char)
            else:
                self.debug_print('\t' + char + ' is literal')
                post += char

        while stack:
            post += stack.pop()

        return post

    # "We will convert a postﬁx regular expression into an NFA using a stack,
    # where each element on the stack is an NFA."
    def post2nfa(self, post):
        self.debug_print('POST2NFA ---------------------------------')
        stack = list()

        for idx, char in enumerate(post):
            if char is '\\':
                self.debug_print('char is escape')

            # TODO: in2post 
            elif char is '.':
                self.debug_print('char is wildcard')

            elif char is '|':
                #e1 = stack.pop()
                #e2 = stack.pop()
                #state = NfaState(Control.split, e1.start, e2.start)
                #stack.append( NfaFrag(state, state.out) )
                #self.debug_print(str(stack))
                self.debug_print('char is pipe')

            else:
                state = NfaState(idx, None, None)
                stack.append( NfaFrag(state, state.out) )
                self.debug_print(str(state))


    def match(self, str):
        pass


if __name__ == '__main__':
    pyre = Pyre(debug=sys.argv[2:])
    pyre.compile(sys.argv[1])
    pyre.match('aab')
