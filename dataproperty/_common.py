# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <gogogo.vm@gmail.com>
"""

from __future__ import absolute_import
from __future__ import unicode_literals
from decimal import Decimal
import itertools

from ._typecode import Typecode


DEFAULT_FLOAT_TYPE = Decimal
DEFAULT_INF_VALUE = DEFAULT_FLOAT_TYPE("inf")
DEFAULT_NAN_VALUE = DEFAULT_FLOAT_TYPE("nan")

DEFAULT_STRICT_TYPE_MAPPING = {
    Typecode.NONE: False,
    Typecode.INTEGER: False,
    Typecode.FLOAT: False,
    Typecode.STRING: False,
    Typecode.DATETIME: True,
    Typecode.INFINITY: False,
    Typecode.NAN: False,
    Typecode.BOOL: False,
    Typecode.DICTIONARY: True,
}
STRICT_TYPE_MAPPING = dict(itertools.product(Typecode.LIST, [True]))
NOT_STRICT_TYPE_MAPPING = dict(itertools.product(Typecode.LIST, [False]))


def default_bool_converter(value):
    return value


def default_datetime_converter(value):
    return value
