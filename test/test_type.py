# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <gogogo.vm@gmail.com>
"""

from dataproperty import *
import pytest


class Test_DataPeroperty_repr:

    @pytest.mark.parametrize(["type_class", "value", "is_strict", "expected"], [
        [
            IntegerType, 0, True,
            "is_type=True, is_strict_type=True, is_convertible_type=True, try_convert=0"
        ],
        [
            IntegerType, "0", True,
            "is_type=False, is_strict_type=False, is_convertible_type=True, try_convert=0"
        ],
        [
            IntegerType, "0", False,
            "is_type=True, is_strict_type=False, is_convertible_type=True, try_convert=0"
        ],
    ])
    def test_normal(self, type_class, value, is_strict, expected):
        type_obj = type_class(value, is_strict)

        assert str(type_obj) == expected
