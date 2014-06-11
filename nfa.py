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

    def __init__(self, start, out):
        self.start = start
        self.out_list = [out]

    def patch(self, out):
        for s in self.out_list:
            s = out


class Metachar(Enum):
    split = 256
    match = 257
