# encoding: utf-8

'''
@author: Tsuyoshi Hombashi
'''


from dataproperty import *
import pytest


class Test_Typecode_get_typecode_from_bitmap:

    @pytest.mark.parametrize(["value", "expected"], [
        [0, Typecode.STRING],
        [int("1", 2), Typecode.INT],
        [int("10", 2), Typecode.FLOAT],
        [int("11", 2), Typecode.FLOAT],
        [int("100", 2), Typecode.STRING],
        [int("101", 2), Typecode.STRING],
        [int("110", 2), Typecode.STRING],
        [int("111", 2), Typecode.STRING],
        [int("1000", 2), Typecode.STRING],
        [int("1001", 2), Typecode.INT],
        [int("1010", 2), Typecode.FLOAT],
        [int("1100", 2), Typecode.STRING],
    ])
    def test_normal(self, value, expected):
        assert Typecode.get_typecode_from_bitmap(value) == expected

    @pytest.mark.parametrize(["value", "expected"], [
        [None, TypeError],
        ["1", TypeError],
    ])
    def test_exception(self, value, expected):
        with pytest.raises(expected):
            assert Typecode.get_typecode_from_bitmap(value)


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
