# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <gogogo.vm@gmail.com>
"""

from __future__ import absolute_import


class Typecode(object):
    NONE = 0
    INT = 1 << 0
    FLOAT = 1 << 1
    STRING = 1 << 2
    DATETIME = 1 << 3
    INFINITY = 1 << 4
    NAN = 1 << 5
    BOOL = 1 << 6

    __TYPENAME_TABLE = {
        NONE:   "NONE",
        INT:    "INT",
        FLOAT:  "FLOAT",
        STRING: "STRING",
        DATETIME: "DATETIME",
        INFINITY: "INFINITY",
        NAN: "NAN",
        BOOL: "BOOL",
    }

    @classmethod
    def get_typename(cls, typecode):
        return cls.__TYPENAME_TABLE.get(typecode)
