# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <gogogo.vm@gmail.com>
"""

from __future__ import absolute_import
from __future__ import unicode_literals

import copy
from decimal import Decimal
import itertools

from typepy import (
    Typecode,
    StrictLevel,
)


NULL_QUOTE_FLAG_MAPPING = {
    Typecode.BOOL: False,
    Typecode.DATETIME: False,
    Typecode.DICTIONARY: False,
    Typecode.REAL_NUMBER: False,
    Typecode.INFINITY: False,
    Typecode.INTEGER: False,
    Typecode.LIST: False,
    Typecode.NAN: False,
    Typecode.NULL_STRING: False,
    Typecode.NONE: False,
    Typecode.STRING: False,
}

STRICT_TYPE_MAPPING = dict(
    itertools.product(Typecode.TYPE_LIST, [StrictLevel.MAX]))
NOT_STRICT_TYPE_MAPPING = dict(
    itertools.product(Typecode.TYPE_LIST, [StrictLevel.MIN]))


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

    STRICT_LEVEL_MAPPING = {
        Typecode.BOOL: 1,
        Typecode.DATETIME: StrictLevel.MAX,
        Typecode.DICTIONARY: StrictLevel.MAX,
        Typecode.REAL_NUMBER: 1,
        Typecode.INFINITY: StrictLevel.MIN,
        Typecode.INTEGER: 1,
        Typecode.LIST: StrictLevel.MAX,
        Typecode.NAN: StrictLevel.MIN,
        Typecode.NONE: StrictLevel.MAX,
        Typecode.NULL_STRING: StrictLevel.MIN,
        Typecode.STRING: StrictLevel.MIN,
    }

    TYPE_VALUE_MAPPING = {
        Typecode.NONE: None,
        Typecode.INFINITY: INF_VALUE,
        Typecode.NAN: NAN_VALUE,
    }


def default_datetime_formatter(value):
    return value.strftime(DefaultValue.DATETIME_FORMAT)
