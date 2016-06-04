# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <gogogo.vm@gmail.com>
"""

from __future__ import absolute_import
from collections import namedtuple

from ._function import is_integer
from ._function import is_float


CreatorTuple = namedtuple("CreatorTuple", "creator typecode")


class Typecode(object):
    NONE = 0
    INT = 1 << 0
    FLOAT = 1 << 1
    STRING = 1 << 2
    DATETIME = 1 << 3

    __TYPENAME_TABLE = {
        NONE:   "NONE",
        INT:    "INT",
        FLOAT:  "FLOAT",
        STRING: "STRING",
        DATETIME: "DATETIME",
    }

    @classmethod
    def get_typecode_from_bitmap(cls, typecode_bitmap):
        typecode_list = [
            cls.STRING,
            cls.FLOAT,
            cls.INT,
            cls.DATETIME,
        ]

        for typecode in typecode_list:
            if typecode_bitmap & typecode:
                return typecode

        return cls.STRING

    @classmethod
    def get_typecode_from_data(cls, data):
        if data is None:
            return cls.NONE

        if is_integer(data):
            return cls.INT

        if is_float(data):
            return cls.FLOAT

        return cls.STRING

    @classmethod
    def get_typename(cls, typecode):
        return cls.__TYPENAME_TABLE.get(typecode)
