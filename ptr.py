#!/usr/bin/env python
# -*- coding: utf-8 -*-

# -----------------------------------------------------------------------------
# ptr.py
#
# This class simulates pointers, i.e. models a memory location. It is useful
# for storing a reference to a value, rather than the value itself.
#
# [1] http://stackoverflow.com/a/1145848/1830334
# -----------------------------------------------------------------------------


class Ptr:

    def __init__(self, obj):
        self.obj = obj

    def get(self):
        return self.obj

    def set(self, obj):
        self.obj = obj
