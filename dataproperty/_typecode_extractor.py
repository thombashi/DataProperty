# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <gogogo.vm@gmail.com>
"""

from __future__ import absolute_import

from ._typecode import Typecode


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
