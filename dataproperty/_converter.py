# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <gogogo.vm@gmail.com>
"""

from __future__ import absolute_import

from ._function import is_float
from ._function import is_integer


def convert_value(value, none_return_value=None):
    if value is None:
        return none_return_value

    if is_integer(value):
        return int(value)

    if is_float(value):
        return float(value)

    return value
