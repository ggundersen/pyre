#!/usr/bin/env python
# -*- coding: utf-8 -*-

# -----------------------------------------------------------------------------
# nfa.py
# -----------------------------------------------------------------------------


from enum import Enum

from ptr import Ptr


class State:
    
    def __init__(self, trans, out1=None, out2=None, id=None):
        self.trans = trans
        
        # These are either assigned pointers to State instances or they are
        # numbers, i.e. 1 or 2, signifying that they are dangling. Otherwise,
        # they are neither pointers nor dangling.
        self.out_ptr1 = Ptr(out1)
        self.out_ptr2 = Ptr(out2)
        self.id = id


class Frag:

    def __init__(self, start, dangling_ptr_list):
        self.start = start
        # `dangling_ptr_list` is a list of dangling `out` properties from the
        # fragment.
        self.dangling_ptr_list = dangling_ptr_list

    def patch(self, new_out_state):
        for ptr in self.dangling_ptr_list:
            ptr.set(new_out_state)
            # This list is only dangling pointers. Remove the `Ptr` instance
            # after setting the pointer.
            self.dangling_ptr_list.remove(ptr)
            

class Metachar(Enum):
    split = 256
    match = 257
