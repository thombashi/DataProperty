# encoding: utf-8

'''
@author: Tsuyoshi Hombashi
'''


from __future__ import absolute_import

import dataproperty


class Typecode:
    NONE = 0
    INT = 1 << 0
    FLOAT = 1 << 1
    STRING = 1 << 2

    __TYPENAME_TABLE = {
        NONE:   "NONE",
        INT:    "INT",
        FLOAT:  "FLOAT",
        STRING: "STRING",
    }

    @classmethod
    def get_typecode_from_bitmap(cls, typecode_bitmap):
        typecode_list = [cls.STRING, cls.FLOAT, cls.INT]

        for typecode in typecode_list:
            if typecode_bitmap & typecode:
                return typecode

        return cls.STRING

    @classmethod
    def get_typecode_from_data(cls, data):
        if data is None:
            return cls.NONE

        if dataproperty.is_integer(data):
            return cls.INT

        if dataproperty.is_float(data):
            return cls.FLOAT

        return cls.STRING

    @classmethod
    def get_typename(cls, typecode):
        return cls.__TYPENAME_TABLE.get(typecode)
