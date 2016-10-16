# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <gogogo.vm@gmail.com>
"""

import pytest

from dataproperty import Typecode


class Test_Typecode_get_typename:

    @pytest.mark.parametrize(["value", "expected"], [
        [Typecode.NONE, "NONE"],
        [Typecode.INT, "INTEGER"],
        [Typecode.INTEGER, "INTEGER"],
        [Typecode.FLOAT, "FLOAT"],
        [Typecode.STRING, "STRING"],
        [Typecode.DATETIME, "DATETIME"],
        [Typecode.INFINITY, "INFINITY"],
        [Typecode.NAN, "NAN"],
        [Typecode.BOOL, "BOOL"],
    ])
    def test_normal(self, value, expected):
        assert Typecode.get_typename(value) == expected

    @pytest.mark.parametrize(["value", "expected"], [
        [Typecode.NONE, "none"],
        [Typecode.INT, "integer"],
        [Typecode.INTEGER, "integer"],
        [Typecode.FLOAT, "float"],
        [Typecode.STRING, "string"],
        [Typecode.DATETIME, "datetime"],
        [Typecode.INFINITY, "infinity"],
        [Typecode.NAN, "nan"],
        [Typecode.BOOL, "bool"],
    ])
    def test_normal_change_typename(self, value, expected):
        Typecode.TYPENAME_TABLE = {
            Typecode.NONE: "none",
            Typecode.INT: "int",
            Typecode.INTEGER: "integer",
            Typecode.FLOAT: "float",
            Typecode.STRING: "string",
            Typecode.DATETIME: "datetime",
            Typecode.INFINITY: "infinity",
            Typecode.NAN: "nan",
            Typecode.BOOL: "bool",
        }
        assert Typecode.get_typename(value) == expected

        Typecode.TYPENAME_TABLE = Typecode.DEFAULT_TYPENAME_TABLE
        assert Typecode.get_typename(value) == expected.upper()

    @pytest.mark.parametrize(["value", "expected"], [
        [0xffff, ValueError],
    ])
    def test_exception(self, value, expected):
        with pytest.raises(expected):
            Typecode.get_typename(value)
