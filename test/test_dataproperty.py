# encoding: utf-8

'''
@author: Tsuyoshi Hombashi
'''

import pytest
import six

import thutils.common
from dataproperty import *


nan = float("nan")
inf = float("inf")


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


class Test_DataPeroperty_data:

    @pytest.mark.parametrize(["value", "expected"], [
        [1, 1],
        ["a", "a"],
        [None, None],
    ])
    def test_normal(self, value, expected):
        dp = DataPeroperty(value)
        assert dp.data == expected


class Test_DataPeroperty_typecode:

    @pytest.mark.parametrize(["value", "expected"], [
        [1, Typecode.INT],
        [1.0, Typecode.FLOAT],
        [123.45, Typecode.FLOAT],
        ["a", Typecode.STRING],
        [None, Typecode.NONE],
        [nan, Typecode.FLOAT],
    ])
    def test_normal(self, value, expected):
        dp = DataPeroperty(value)
        assert dp.typecode == expected


class Test_DataPeroperty_align:

    @pytest.mark.parametrize(["value", "expected"], [
        [1, Align.RIGHT],
        [1.0, Align.RIGHT],
        ["a", Align.LEFT],
        [None, Align.LEFT],
        [nan, Align.RIGHT],
    ])
    def test_normal(self, value, expected):
        dp = DataPeroperty(value)
        assert dp.align == expected


class Test_DataPeroperty_str_len:

    @pytest.mark.parametrize(["value", "expected"], [
        [1, 1],
        [1.0, 3],
        [12.34, 5],
        ["a", 1],
        [None, 4],
    ])
    def test_normal(self, value, expected):
        dp = DataPeroperty(value)
        assert dp.str_len == expected

    @pytest.mark.parametrize(["value", "expected"], [
        [nan, nan],
    ])
    def test_abnormal(self, value, expected):
        dp = DataPeroperty(value)
        thutils.common.is_nan(dp.str_len)


class Test_DataPeroperty_integer_digits:

    @pytest.mark.parametrize(["value", "expected"], [
        [1, 1],
        [1.0, 1],
        [12.34, 2],
    ])
    def test_normal(self, value, expected):
        dp = DataPeroperty(value)
        assert dp.integer_digits == expected

    @pytest.mark.parametrize(["value"], [
        [None],
        ["a"],
        [nan],
    ])
    def test_abnormal(self, value):
        dp = DataPeroperty(value)
        thutils.common.is_nan(dp.integer_digits)


class Test_DataPeroperty_decimal_places:

    @pytest.mark.parametrize(["value", "expected"], [
        [1, 0],
        [1.0, 1],
        [12.34, 2],
    ])
    def test_normal(self, value, expected):
        dp = DataPeroperty(value)
        assert dp.decimal_places == expected

    @pytest.mark.parametrize(["value"], [
        [None],
        ["a"],
        [nan],
    ])
    def test_abnormal(self, value):
        dp = DataPeroperty(value)
        thutils.common.is_nan(dp.decimal_places)


# PropertyExtractor class ---

class Test_PropertyExtractor_get_align_from_typecode:

    @pytest.mark.parametrize(["value", "expected"], [
        [Typecode.STRING, Align.LEFT],
        [Typecode.INT, Align.RIGHT],
        [Typecode.FLOAT, Align.RIGHT],
    ])
    def test_normal(self, value, expected):
        assert PropertyExtractor.get_align_from_typecode(value) == expected


class Test_PropertyExtractor_extract_data_property_matrix:

    @pytest.mark.parametrize(["value"], [
        [
            [
                [None, 1],
                [1.0, "a"],
            ],
        ],
    ])
    def test_normal(self, value):
        prop_matrix = PropertyExtractor.extract_data_property_matrix(value)

        assert len(prop_matrix) == 2
        assert prop_matrix[0][0].typecode == Typecode.NONE
        assert prop_matrix[0][1].typecode == Typecode.INT
        assert prop_matrix[1][0].typecode == Typecode.FLOAT
        assert prop_matrix[1][1].typecode == Typecode.STRING

    @pytest.mark.parametrize(["value", "expected"], [
        [None, TypeError],
    ])
    def test_exception(self, value, expected):
        with pytest.raises(expected):
            PropertyExtractor.extract_data_property_matrix(value)


class Test_PropertyExtractor_extract_column_property_list:

    @pytest.mark.parametrize(["header_list", "value"], [
        [
            ["i", "f", "s", "if", "mix"],
            [
                [1, 1.1, "aaa", 1,   1],
                [2, 2.2, "bbb", 2.2, 2.2],
                [3, 3.3, "ccc", 3,   "ccc"],
            ],
        ],
        [
            None,
            [
                [1, 1.1, "aaa", 1,   1],
                [2, 2.2, "bbb", 2.2, 2.2],
                [3, 3.3, "ccc", 3,   "ccc"],
            ],
        ],
    ])
    def test_normal(self, header_list, value):
        col_prop_list = PropertyExtractor.extract_column_property_list(
            header_list, value)

        assert len(col_prop_list) == 5
        assert col_prop_list[0].typecode == Typecode.INT
        assert col_prop_list[1].typecode == Typecode.FLOAT
        assert col_prop_list[2].typecode == Typecode.STRING
        assert col_prop_list[3].typecode == Typecode.FLOAT
        assert col_prop_list[4].typecode == Typecode.STRING

    @pytest.mark.parametrize(["header_list", "value", "expected"], [
        [
            None,
            None,
            TypeError
        ],
        [
            ["i", "f", "s", "if", "mix"],
            None,
            TypeError
        ],
    ])
    def test_exception(self, header_list, value, expected):
        with pytest.raises(expected):
            PropertyExtractor.extract_column_property_list(
                header_list, value)
