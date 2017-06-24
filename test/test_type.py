# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

import pytest
from typepy import StrictLevel
from typepy.type import Integer


class Test_DataPeroperty_repr(object):

    @pytest.mark.parametrize(
        ["type_class", "value", "strict_level", "expected"],
        [
            [
                Integer, 0, StrictLevel.MAX,
                "is_type=True, strict_level=100, try_convert=0"
            ],
            [
                Integer, "0", StrictLevel.MAX,
                "is_type=False, strict_level=100, try_convert=None"
            ],
            [
                Integer, "0", StrictLevel.MIN,
                "is_type=True, strict_level=0, try_convert=0"
            ],
        ])
    def test_normal(self, type_class, value, strict_level, expected):
        type_obj = type_class(value, strict_level=strict_level)

        assert str(type_obj) == expected
