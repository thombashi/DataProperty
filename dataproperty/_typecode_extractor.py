# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <gogogo.vm@gmail.com>
"""

from __future__ import absolute_import

from ._typecode import Typecode
from ._type_checker_creator import IntegerTypeCheckerCreator
from ._type_checker_creator import FloatTypeCheckerCreator
from ._type_checker_creator import DateTimeTypeCheckerCreator


_checker_creator_list = [
    IntegerTypeCheckerCreator(),
    FloatTypeCheckerCreator(),
    DateTimeTypeCheckerCreator()
]


def get_typecode_from_data(data, is_convert=True):
    if data is None:
        return Typecode.NONE

    for checker_creator in _checker_creator_list:
        checker = checker_creator.create(data, is_convert)
        if checker.is_type():
            return checker.typecode

    return Typecode.STRING
