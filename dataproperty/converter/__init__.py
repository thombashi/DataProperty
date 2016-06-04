# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <gogogo.vm@gmail.com>
"""

from __future__ import absolute_import
from collections import namedtuple

from ._core import IntegerConverter
from ._core import FloatConverter
from ._core import DateTimeConverter
from ._creator import IntegerConverterCreator
from ._creator import FloatConverterCreator
from ._creator import DateTimeConverterCreator
from .._type_checker_creator import IntegerTypeCheckerCreator
from .._type_checker_creator import FloatTypeCheckerCreator
from .._type_checker_creator import DateTimeTypeCheckerCreator


_ConverterFactory = namedtuple(
    "ConverterFactory", "type_checker_factory value_converter_factory")

_type_factory_list = [
    _ConverterFactory(
        IntegerTypeCheckerCreator(), IntegerConverterCreator()),
    _ConverterFactory(
        FloatTypeCheckerCreator(), FloatConverterCreator()),
    _ConverterFactory(
        DateTimeTypeCheckerCreator(), DateTimeConverterCreator()),
]


def convert_value(value, none_return_value=None, is_convert=True):
    if value is None:
        return none_return_value

    for type_factory in _type_factory_list:
        if type_factory.type_checker_factory.create(value, is_convert).is_type():
            return type_factory.value_converter_factory.create(
                value, is_convert).convert()

    return value
