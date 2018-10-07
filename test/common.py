# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

from __future__ import absolute_import

from dataproperty._common import NOT_STRICT_TYPE_MAP, STRICT_TYPE_MAP


def get_strict_type_map(is_strict):
    return STRICT_TYPE_MAP if is_strict else NOT_STRICT_TYPE_MAP
