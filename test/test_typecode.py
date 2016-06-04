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
        [0xffff, None],
    ])
    def test_normal(self, value, expected):
        assert Typecode.get_typename(value) == expected
