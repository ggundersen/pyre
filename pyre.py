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
# [5] http://perl.plover.com/Regex/article.html
# [6] http://www.codeproject.com/Articles/5412/Writing-own-regular-expression-parser#Seven
# -----------------------------------------------------------------------------


import sys
import pdb

from ptr import Ptr
from nfa import State, Frag, Metachar


class Pyre:


    def __init__(self, input_re, debug=False):
        self.debug = debug
        self.metachars = {
            'infix': {
                '|': 9
            },
            '*': 8,
            '+': 7,
            '?': 6,
            '^': 5,
            '$': 4,
            '(': 0,
            ')': 0
        }
        self.list_id = 0
        self.start_ptr = None

        self.compile(input_re)


    def pprint(self, msg):
        if (self.debug):
            print(msg)


    # TODO: What happens if the client executes `match` twice? Does `start_ptr`
    # need to be reset?
    def compile(self, input_re):
        """Converts a postfix expression to an NFA and sets the start pointer
        for `match`.

        Args: `re`, an infix expression.

        Returns: void but sets the start pointer for the Pyre instance.
        """

        self.pprint('Compiling ' + input_re)
        self.re_store = input_re
        postfix_re = self.in2post(input_re)
        self.start_ptr = self.post2nfa(postfix_re)


    def prec(self, char):
        """Calculates operator precedence. See [4].
        """
        return self.metachars[char]


    # TODO: Should convert implicit concatentation, e.g. AB, into explicit
    # concatentation, e.g. A&B 
    def in2post(self, input_str):
        """Converts an infix expression to a postfix expression.

        Why? Postfix notation is useful because parentheses are unneeded since
        the notation does not have the operator-operand ambiguity inherent to
        inﬁx expressions [1].

        We will use "&" for an explicit concatentation operator. Ken Thompson
        originally used "."[2], but we want to use the dot as a wild card. 

        This function's algorithm is from [3].

        Args: An infix expression, e.g. a+b.

        Returns: A postfix expression converted from the input, e.g. ab+.
        """

        post = ''
        stack = []

        for char in input_str:
            if char in self.metachars['infix']:
                self.pprint(char + ' is in the list of operators')
                if not stack:
                    self.pprint('\t' + 'stack empty, placing onto stack')
                    stack.append(char)
                # If `char` has a higher precedence than the top of the stack:
                elif self.prec(char) > self.prec(stack[-1]):
                    self.pprint('\t' + char + ' has higher precedence, placed onto stack')
                    stack.append(char)
                # If `char` has a lower precedence:
                else:
                    # If we see an open paren, do not pop operators off stack.
                    if char is self.metachars['(']:
                        # Place open paren on stack as a marker
                        self.pprint('\topen paren found, placing on stack')
                        stack.append(char)
                    elif char is self.metachars[')']:
                        # TODO: What if there is no open paren?
                        self.pprint('\tclose paren found, pop stack until find open paren')
                        while stack and stack[-1] is not self.metachars['(']:
                            post += stack.pop()
                        # Remove open paren
                        stack.pop()
                    else:
                        while stack and self.prec(char) <= self.prec(stack[-1]):
                            self.pprint('\t' + char + ' has lower or equal precedence than ' + stack[-1] + ', pop top of stack')
                            post += stack.pop()
                            self.pprint('\t\t' + str(stack))
                            self.pprint('\t\t' + post)
                        stack.append(char)
            else:
                self.pprint(char + ' is literal')
                post += char
        
        while stack:
            post += stack.pop()
        
        return post


    def post2nfa(self, post):
        """Converts a postfix expression to an NFA.

        Args: A postfix expression, e.g. ab+ rather than a+b.

        Returns: A pointer to the NFA start state.
        """
        stack = []
        for char in post:
            if char is '+':
                # Remove the NFA fragment currently on the stack. This is the
                # state that we want to repeat. 
                f = stack.pop()
  
                # Create a new NFA state in which the first out state is the
                # state we want to repeat. This creates the loopback.
                s = State(Metachar.split, f.start)

                # Patch the dangling out states of the previous fragment to the
                # newly created state. This completes the loop.
                f.patch(s)
                
                # Add the new fragment onto the stack.
                stack.append( Frag(f.start, [s.out_ptr2]) )

            # Concatentation. This is the important step, because it reduces
            # the number of NFA fragments on the stack.
            elif char is '&':
                f2 = stack.pop()
                f1 = stack.pop()
                f1.patch(f2.start)
                stack.append( Frag(f1.start, f2.dangling_ptr_list) )

            # Character literals
            else:
                s = State(char, True)
                stack.append( Frag(s, [s.out_ptr1]) )

        # In [2] this line of code is a `pop`, but that just shifts the stack
        # pointer. I don't think we actually want to remove this NFA fragment
        # from the stack. 
        nfa = stack[-1]
        nfa.patch( State(Metachar.match) )
        return Ptr(nfa.start)

    
    def match(self, str):
 
        curr_list_ptr = Ptr([ self.start_ptr ])
        next_list_ptr = Ptr([])

        for char in str:
            self.step(curr_list_ptr, char, next_list_ptr);
            # We swap lists because on the next iteration of this loop, we need
            # `next_list_ptr` to be the current list of states. We then reuse
            # `curr_list_ptr`.
            temp = curr_list_ptr
            curr_list_ptr = next_list_ptr
            next_list_ptr = temp

        is_a_match = self.is_match(curr_list_ptr)
        if is_a_match:
            print(self.re_store + ' matches ' + str)
        else:
            print(self.re_store + ' does *not* match ' + str)


    def step(self, curr_list_ptr, char, next_list_ptr):
        self.list_id += 1
        clist = curr_list_ptr.get()
        for ptr in clist:
            state = ptr.get()
            if state.trans == char:
                self.add_state(next_list_ptr, state.out_ptr1)


    def add_state(self, next_list_ptr, state_ptr):
        state = state_ptr.get()
        if state == None or state.id == self.list_id:
            return
        state.id = self.list_id
        if (state.trans == Metachar.split):
            self.add_state(next_list_ptr, state.out_ptr1)
            self.add_state(next_list_ptr, state.out_ptr2)
            return
        next_list_ptr.get().append(state_ptr)

    
    def is_match(self, states_ptr):
        states = states_ptr.get()
        for s_p in states:
            if s_p.get().trans == Metachar.match:
                return True
        return False


if __name__ == '__main__':
    if len(sys.argv) == 4:
        use_debug = (sys.argv[3] == 'True')
    else:
        use_debug = False

    pyre = Pyre(sys.argv[1], use_debug)
    pyre.match(sys.argv[2])
