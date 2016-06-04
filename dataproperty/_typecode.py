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

    __TYPENAME_TABLE = {
        NONE:   "NONE",
        INT:    "INT",
        FLOAT:  "FLOAT",
        STRING: "STRING",
        DATETIME: "DATETIME",
    }

    @classmethod
    def get_typename(cls, typecode):
        return cls.__TYPENAME_TABLE.get(typecode)


class _TypecodeExtractor(object):

    def __init__(self):
        from ._type_checker_creator import IntegerTypeCheckerCreator
        from ._type_checker_creator import FloatTypeCheckerCreator
        from ._type_checker_creator import DateTimeTypeCheckerCreator

        self.__checker_creator_list = [
            IntegerTypeCheckerCreator(),
            FloatTypeCheckerCreator(),
            DateTimeTypeCheckerCreator()
        ]

    def get_typecode_from_bitmap(self, typecode_bitmap):
        typecode_list = [
            Typecode.STRING,
            Typecode.FLOAT,
            Typecode.INT,
            Typecode.DATETIME,
        ]

        for typecode in typecode_list:
            if typecode_bitmap & typecode:
                return typecode

        return Typecode.STRING

    def get_typecode_from_data(self, data, is_convert=True):
        if data is None:
            return Typecode.NONE

        for checker_creator in self.__checker_creator_list:
            checker = checker_creator.create(data, is_convert)
            if checker.is_type():
                return checker.typecode

        return Typecode.STRING


typecode_extractor = _TypecodeExtractor()
