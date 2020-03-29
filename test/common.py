"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

from dataproperty._common import MAX_STRICT_LEVEL_MAP, MIN_STRICT_LEVEL_MAP


def get_strict_level_map(is_strict):
    return MAX_STRICT_LEVEL_MAP if is_strict else MIN_STRICT_LEVEL_MAP
