# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <gogogo.vm@gmail.com>
"""

from __future__ import absolute_import
from collections import namedtuple

from ._creator import IntegerConverterCreator
from ._creator import FloatConverterCreator
from ._creator import DateTimeConverterCreator

from ._factory import IntegerTypeFactory
from ._factory import FloatTypeFactory
from ._factory import DateTimeTypeFactory


_type_factory_list = [
    IntegerTypeFactory(),
    FloatTypeFactory(),
    DateTimeTypeFactory(),
]


def convert_value(value, none_return_value=None, is_convert=True):
    if value is None:
        return none_return_value

    for type_factory in _type_factory_list:
        if type_factory.type_checker_factory.create(value, is_convert).is_type():
            return type_factory.value_converter_factory.create(
                value, is_convert).convert()

    return value
