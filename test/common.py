# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

from __future__ import absolute_import

from dataproperty._common import NOT_STRICT_TYPE_MAPPING, STRICT_TYPE_MAPPING


def get_strict_type_mapping(is_strict):
    return STRICT_TYPE_MAPPING if is_strict else NOT_STRICT_TYPE_MAPPING
