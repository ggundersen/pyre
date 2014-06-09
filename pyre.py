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
    
    def __init__(self, control, out1, out2, last_list=None):
        self.control = control
        # out1 and out2 are `OutList`s, list of references to out states.
        self.out1 = out1
        self.out2 = out2
        self.last_list = last_list


class NfaFrag:

    def __init__(self, start, out_list):
        self.start = start
        self.out_list = out_list


class OutList:

    def __init__(self, out):
        self.l = [out]

    def patch(self, state):
        for ptr in self.l:
            ptr = state

    def append(self, l2):
        return self.l + l2


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
        stack = []

        for char in in_str:
            if char in self.operators:
                self.debug_print(char + ' is in the list of operators')
                if not stack:
                    self.debug_print('\t' + 'stack empty, placing onto stack')
                    stack.append(char)
                # If `char` has a higher precedence than the top of the stack:
                elif self.prec(char) > self.prec(stack[-1]):
                    self.debug_print('\t' + char + ' has higher precedence, placed onto stack')
                    stack.append(char)
                # If `char` has a lower precedence:
                else:
                    # If we see an open paren, do not pop operators off stack.
                    if char is '(':
                        # Place open paren on stack as a marker
                        self.debug_print('\topen paren found, placing on stack')
                        stack.append(char)
                    elif char is ')':
                        # TODO: What if there is no open paren?
                        self.debug_print('\tclose paren found, pop stack until find open paren')
                        while stack and stack[-1] is not '(':
                            post += stack.pop()
                        # Remove open paren
                        stack.pop()
                    else:
                        while stack and self.prec(char) <= self.prec(stack[-1]):
                            self.debug_print('\t' + char + ' has lower or equal precedence than ' + stack[-1] + ', pop top of stack')
                            post += stack.pop()
                            self.debug_print('\t\t' + str(stack))
                            self.debug_print('\t\t' + post)
                        stack.append(char)
            else:
                self.debug_print(char + ' is literal')
                post += char
        
        while stack:
            post += stack.pop()
        
        return post

    # "We will convert a postﬁx regular expression into an NFA using a stack,
    # where each element on the stack is an NFA."
    def post2nfa(self, post):
        self.debug_print('POST2NFA ---------------------------------')
        stack = []

        for idx, char in enumerate(post):

# -----------------------------------------------------------------------------
            # e+ matches one or more e's. Notice that we 
            if char is '+':
                # Remove the NFA fragment currently on the stack. This is the
                # one that we want to repeat. 
                e = stack.pop()
                # Create a new NFA state in which the first out state is e, the
                # previous state. This represents the loop. 
                s = NfaState(Control.split, e.start, None)
                # Patch takes the dangling out states of e and points them to
                # s. This 'patches' the NFA fragments into a larger fragment. 
                e.out_list.patch(s)
                stack.append( NfaFrag(s, s.out1) )
                self.debug_print(str(stack))

            # This block builds the start state, and should only be execute
            # once.
            else:
                s = NfaState(idx, None, None)
                stack.append( NfaFrag(s, OutList(s.out1)) )
                self.debug_print( str(stack) )


    def match(self, str):
        pass


if __name__ == '__main__':
    pyre = Pyre(debug=sys.argv[2:])
    pyre.compile(sys.argv[1])
    pyre.match('aab')
