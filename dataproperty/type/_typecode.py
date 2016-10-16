# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <gogogo.vm@gmail.com>
"""

from __future__ import absolute_import


class Typecode(object):
    NONE = 0
    INT = 1 << 0  # delete in the future
    INTEGER = 1 << 0
    FLOAT = 1 << 1
    STRING = 1 << 2
    DATETIME = 1 << 3
    INFINITY = 1 << 4
    NAN = 1 << 5
    BOOL = 1 << 6

    DEFAULT_TYPENAME_TABLE = {
        NONE: "NONE",
        INT: "INTEGER",
        INTEGER: "INTEGER",
        FLOAT: "FLOAT",
        STRING: "STRING",
        DATETIME: "DATETIME",
        INFINITY: "INFINITY",
        NAN: "NAN",
        BOOL: "BOOL",
    }

    TYPENAME_TABLE = DEFAULT_TYPENAME_TABLE

    @classmethod
    def get_typename(cls, typecode):
        type_name = cls.TYPENAME_TABLE.get(typecode)
        if type_name is None:
            raise ValueError("unknown typecode: {}".format(typecode))

        return type_name
