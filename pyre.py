#!/usr/bin/env python
# -*- coding: utf-8 -*-

# -----------------------------------------------------------------------------
# pyre.py
# A Python implementation of a regular expression engine.
#
# [1]  http://ezekiel.vancouver.wsu.edu/~cs317/archive/projects/grep/grep.pdf
# [2]  http://swtch.com/~rsc/regexp/regexp1.html
# [2b] http://swtch.com/~rsc/regexp/nfa.c.txt
# [3]  http://csis.pace.edu/~wolf/CS122/infix-postfix.htm
# [4]  http://stackoverflow.com/q/60208/1830334
# [5]  http://perl.plover.com/Regex/article.html
# [6]  http://www.codeproject.com/Articles/5412/Writing-own-regular-expression-parser#Seven
# -----------------------------------------------------------------------------


import sys
import pdb

from ptr import Ptr
from nfa import State, Frag, Metachar


class Pyre:


    def __init__(self, input_re, debug=False):
        self.debug = debug
        self.operators = {
            '&': 9,
            '|': 8,
            '*': 7,
            '+': 6
        }
        self.list_id = 0
        self.start_ptr = None

        self.__compile(input_re)

  
    def match(self, string_to_match):
        """TODO docstring.
        """

        # Initialize the `curr_list_ptr` to point to a list with a single
        # pointer, the start state. This handles an operator being the start
        # state.
        curr_list_ptr = self.__start_list(Ptr([]), self.start_ptr)

        # Empty until set in `__step()`.
        next_list_ptr = Ptr([])

        for char in string_to_match:
            self.__step(curr_list_ptr, char, next_list_ptr)

            # We swap lists because on the next iteration of this loop, we need
            # `next_list_ptr` to be the current list of states. We then reuse
            # `curr_list_ptr`.
            temp = curr_list_ptr
            curr_list_ptr = next_list_ptr
            next_list_ptr = temp

        if self.__has_match(curr_list_ptr):
            print(self.re_store + ' matches ' + string_to_match)
        else:
            print(self.re_store + ' does not match ' + string_to_match)

    
    def __start_list(self, list_ptr, start_ptr):
        """Initializes the pointer list. Importantly, by calling `add_state()`
        immediately, it handles any operators at the beginning of the NFA, i.e.
        the Boolean OR.
        """

        self.list_id += 1
        self.__add_state(list_ptr, start_ptr)
        return list_ptr


    def __step(self, curr_list_ptr, char, next_list_ptr):
        """Advances the NFA simulation a single character. It uses the current
        list of pointers to calculate the next. Notice that it passes
        `next_list_ptr` into `__add_state()`.
        """

        self.list_id += 1
        curr_list = curr_list_ptr.get()
        for ptr in curr_list:
            state = ptr.get()

            # If the current state's transition is the same as the character
            # being parsed:
            if state.trans == char:
                self.__add_state(next_list_ptr, state.out_ptr1)


    def __add_state(self, list_ptr, state_ptr):
        """Adds a state pointer to a list of state pointers but only if the
        state was not previously added.
        """

        state = state_ptr.get()

        # `id` prevents us from adding a state more than once to the same list.
        if state == None or state.id == self.list_id:
            return
        state.id = self.list_id
        if state.trans == Metachar.split:
            self.__add_state(list_ptr, state.out_ptr1)
            self.__add_state(list_ptr, state.out_ptr2)
            return
        list_ptr.get().append(state_ptr)


    def __has_match(self, list_ptr):
        """Checks a list of state pointers for a transition that is `match`; in
        other words, leads to an accepting state.

        Args: `list_ptr`, a list of state pointers.

        Returns: True or False based on the condition above.
        """

        states = list_ptr.get()
        for state_ptr in states:
            if state_ptr.get().trans == Metachar.match:
                return True
        return False


    # TODO: What happens if the client executes `match` twice? Does `start_ptr`
    # need to be reset?
    def __compile(self, input_re):
        """Converts a postfix expression to an NFA and sets the start pointer
        for `match`.

        Args: `re`, an infix expression.

        Returns: void but sets the start pointer for the Pyre instance.
        """

        #self.__print('\npyre\n====\n')
        #self.__print('compiling infix expression: ' + input_re)
        self.re_store = input_re
        postfix_re = self.__in2post(input_re)
        #self.__print('postfix expression generated: ' + postfix_re)
        self.start_ptr = self.__post2nfa(postfix_re)


    def __in2post(self, input_str):
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
            if char in self.operators:
                #self.__print(char + ' is in the list of operators')

                if len(stack) == 0:
                    #self.__print('\t stack empty, placing onto stack')
                    stack.append(char)
                    #self.__print('\t stack: ' + str(stack))

                # If `char` has a higher precedence than the top of the stack:
                elif self.__prec(char) > self.__prec(stack[-1]):
                    # Place the new operator on the stack so that it will come
                    # first after the stack is popped. For example, if the
                    # input is A+B*C, and we are parsing the "*", we should see
                    # "+" on the stack and then place "*" on top. When we pop
                    # the stack at end of this function, we'll reverse those
                    # two to produce "ABC*+".
                    #self.__print('\t' + char + ' has higher precedence than ' + stack[-1] + '; ' + char + ' placed onto stack')
                    stack.append(char)
                    #self.__print('\t stack: ' + str(stack))

                # If `char` has a lower precedence:
                else:
                    #self.__print('\t' + char + ' has lower precedence than ' + stack[-1])
                    # If we see an open paren, do not pop operators off stack.
                    if char is '(':
                        # Place open paren on stack as a marker
                        # self.__print('\topen paren found, placing on stack')
                        stack.append(char)
                    elif char is ')':
                        # TODO: What if there is no open paren?
                        # self.__print('\tclose paren found, pop stack until find open paren')
                        while stack and stack[-1] is not self.metachars['(']:
                            post += stack.pop()
                        # Remove open paren
                        stack.pop()
                    else:
                        while stack and self.__prec(char) <= self.__prec(stack[-1]):
                            #self.__print('\t' + char + ' has lower or equal precedence than ' + stack[-1] + ', pop top of stack')
                            post += stack.pop()
                            #self.__print('\t\tstack: ' + str(stack))
                            #self.__print('\t\tpostfix: ' + post)
                        stack.append(char)
            else:
                # Handle conversion of implicit to explicit concatenation.
                #self.__print(char + ' is a literal')
                #self.__print('\texplicit concatenation')
                if post != '' and post[-1] not in self.operators:
                    #self.__print('\tadding & to stack')
                    stack.append('&')
                post += char

        while stack:
            post += stack.pop()
        
        return post


    def __post2nfa(self, post):
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

            # Boolean "or". We create a new NFA fragment with two out pointers,
            # one to each start state of the previous two fragments.
            elif char is '|':
                f2 = stack.pop()
                f1 = stack.pop()
                s = State(Metachar.split, f1.start, f2.start)
                stack.append( Frag(s, f1.dangling_ptr_list + f2.dangling_ptr_list) )

            # Character literals
            else:
                # We pass in `True` to capture a value, i.e. we cannot point to
                # null.
                s = State(char, True)
                stack.append( Frag(s, [s.out_ptr1]) )

        # There should be only one fragment on the stack.
        nfa = stack.pop()
        nfa.patch( State(Metachar.match) )
        return Ptr(nfa.start)

    
    def __prec(self, operator):
        """Calculates operator precedence. See [4].

        Returns: the a number that represents the precedence of the operator.
        """
        return self.operators[operator]


    def __print(self, msg):
        """Prints only in debug mode.
        """
        if (self.debug):
            print(msg)


if __name__ == '__main__':
    # Default to True for now.
    #if len(sys.argv) == 4:
    #    use_debug = (sys.argv[3] == 'True')
    #else:
    #    use_debug = False

    pyre = Pyre(sys.argv[1], True)
    pyre.match(sys.argv[2])
