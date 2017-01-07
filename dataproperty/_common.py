# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <gogogo.vm@gmail.com>
"""

from __future__ import absolute_import
from __future__ import unicode_literals
import copy
import itertools

import six

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


def default_datetime_formatter(value):
    from ._enum import DEFAULT_DATETIME_FORMAT

    return value.strftime(DEFAULT_DATETIME_FORMAT)
