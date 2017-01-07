# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <gogogo.vm@gmail.com>
"""

from __future__ import absolute_import
from __future__ import unicode_literals
import copy
from decimal import Decimal
import itertools

from ._typecode import Typecode


NULL_QUOTE_FLAG_MAPPING = {
    Typecode.NONE: False,
    Typecode.INTEGER: False,
    Typecode.FLOAT: False,
    Typecode.STRING: False,
    Typecode.NULL_STRING: False,
    Typecode.DATETIME: False,
    Typecode.FLOAT: False,
    Typecode.NAN: False,
    Typecode.BOOL: False,
}

STRICT_TYPE_MAPPING = dict(itertools.product(Typecode.LIST, [True]))
NOT_STRICT_TYPE_MAPPING = dict(itertools.product(Typecode.LIST, [False]))


class DefaultValue(object):
    DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%S%z"
    FLOAT_TYPE = Decimal
    INF_VALUE = FLOAT_TYPE("inf")
    NAN_VALUE = FLOAT_TYPE("nan")

    CONST_VALUE_MAPPING = {
        True: True,
        False: False,
    }

    QUOTE_FLAG_MAPPING = copy.deepcopy(NULL_QUOTE_FLAG_MAPPING)

    STRICT_TYPE_MAPPING = {
        Typecode.NONE: False,
        Typecode.INTEGER: False,
        Typecode.FLOAT: False,
        Typecode.STRING: False,
        Typecode.NULL_STRING: False,
        Typecode.DATETIME: True,
        Typecode.INFINITY: False,
        Typecode.NAN: False,
        Typecode.BOOL: False,
        Typecode.DICTIONARY: True,
    }

    TYPE_VALUE_MAPPING = {
        Typecode.NONE: None,
        Typecode.INFINITY: INF_VALUE,
        Typecode.NAN: NAN_VALUE,
    }


def default_datetime_formatter(value):
    return value.strftime(DefaultValue.DATETIME_FORMAT)
