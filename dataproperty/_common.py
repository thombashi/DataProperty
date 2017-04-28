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
        Typecode.NONE: StrictLevel.MAX,
        Typecode.INTEGER: 1,
        Typecode.FLOAT: 1,
        Typecode.STRING: StrictLevel.MIN,
        Typecode.NULL_STRING: StrictLevel.MIN,
        Typecode.DATETIME: StrictLevel.MAX,
        Typecode.INFINITY: StrictLevel.MIN,
        Typecode.NAN: StrictLevel.MIN,
        Typecode.BOOL: 1,
        Typecode.DICTIONARY: StrictLevel.MAX,
    }

    TYPE_VALUE_MAPPING = {
        Typecode.NONE: None,
        Typecode.INFINITY: INF_VALUE,
        Typecode.NAN: NAN_VALUE,
    }


def default_datetime_formatter(value):
    return value.strftime(DefaultValue.DATETIME_FORMAT)
