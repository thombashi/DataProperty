# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <gogogo.vm@gmail.com>
"""

import pytest

from dataproperty import Typecode


class Test_Typecode_get_typename:

    @pytest.mark.parametrize(["value", "expected"], [
        [Typecode.NONE, "NONE"],
        [Typecode.INT, "INT"],
        [Typecode.FLOAT, "FLOAT"],
        [Typecode.STRING, "STRING"],
    ])
    def test_normal(self, value, expected):
        assert Typecode.get_typename(value) == expected

    @pytest.mark.parametrize(["value", "expected"], [
        [0xffff, ValueError],
    ])
    def test_exception(self, value, expected):
        with pytest.raises(expected):
            Typecode.get_typename(value)
