#!/usr/bin/env python
# -*- coding: utf-8 -*-

# -----------------------------------------------------------------------------
# nfa.py
#
# TODO: Should this just be an NFA class?
# -----------------------------------------------------------------------------


from enum import Enum


class State:
    
    def __init__(self, char, out1, out2, id=None):
        self.char = char
        self.out1 = out1
        self.out2 = out2
        self.id = id


class Frag:

    def __init__(self, start, out_list):
        self.start = start
        self.out_list = OutList(out_list)


class OutList:

    def __init__(self, out_state):
        self.lst = [out_state]

    def patch(self, next_state):
        for out_state in self.lst:
            out_state = next_state

    @staticmethod
    def append(out_list1, out_list2):
        return OutList(out_list1 + out_list2)


class Metachar(Enum):
    split = 256
    match = 257
