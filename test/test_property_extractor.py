# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <gogogo.vm@gmail.com>
"""

import datetime
from decimal import Decimal

import pytest

from dataproperty import *


nan = float("nan")
inf = float("inf")


@pytest.fixture
def prop_extractor():
    return PropertyExtractor()


def bool_converter_test(value):
    return str(value).lower()


def datetime_converter_test(value):
    return value.strftime("%Y%m%d %H%M%S")


class Test_PropertyExtractor_extract_data_property_matrix:

    @pytest.mark.parametrize(
        [
            "value", "none_value", "inf_value", "nan_value",
            "bool_converter", "datetime_converter",
        ],
        [
            [
                [
                    [None, "1"],
                    ["1.1", "a"],
                    [nan, inf],
                    ["false", datetime.datetime(2017, 1, 1, 0, 0, 0)]
                ],
                "null",
                "Infinity",
                "NaN",
                bool_converter_test,
                datetime_converter_test,
            ],
        ])
    def test_normal(
            self, prop_extractor, value, none_value, inf_value, nan_value,
            bool_converter, datetime_converter):
        prop_extractor.data_matrix = value
        prop_extractor.none_value = none_value
        prop_extractor.inf_value = inf_value
        prop_extractor.nan_value = nan_value
        prop_extractor.bool_converter = bool_converter_test
        prop_extractor.datetime_converter = datetime_converter
        prop_extractor.datetime_format_str = "s"
        prop_matrix = prop_extractor.extract_data_property_matrix()

        assert len(prop_matrix) == 4

        prop = prop_matrix[0][0]
        assert prop.data == "null"
        assert prop.typecode == Typecode.NONE
        assert prop.align.align_code == Align.LEFT.align_code
        assert prop.align.align_string == Align.LEFT.align_string
        assert prop.str_len == 4
        assert is_nan(prop.decimal_places)
        assert prop.format_str == ""

        prop = prop_matrix[0][1]
        assert prop.data == 1
        assert prop.typecode == Typecode.INT
        assert prop.align.align_code == Align.RIGHT.align_code
        assert prop.align.align_string == Align.RIGHT.align_string
        assert prop.str_len == 1
        assert prop.decimal_places == 0
        assert prop.format_str == "d"

        prop = prop_matrix[1][0]
        assert prop.data == Decimal("1.1")
        assert prop.typecode == Typecode.FLOAT
        assert prop.align.align_code == Align.RIGHT.align_code
        assert prop.align.align_string == Align.RIGHT.align_string
        assert prop.str_len == 3
        assert prop.decimal_places == 1
        assert prop.format_str == ".1f"

        prop = prop_matrix[1][1]
        assert prop.data == "a"
        assert prop.typecode == Typecode.STRING
        assert prop.align.align_code == Align.LEFT.align_code
        assert prop.align.align_string == Align.LEFT.align_string
        assert prop.str_len == 1
        assert is_nan(prop.decimal_places)
        assert prop.format_str == "s"

        prop = prop_matrix[2][0]
        assert prop.data == "NaN"
        assert prop.typecode == Typecode.NAN
        assert prop.align.align_code == Align.LEFT.align_code
        assert prop.align.align_string == Align.LEFT.align_string
        assert prop.str_len == 3
        assert is_nan(prop.decimal_places)
        assert prop.format_str == "f"

        prop = prop_matrix[2][1]
        assert prop.data == "Infinity"
        assert prop.typecode == Typecode.INFINITY
        assert prop.align.align_code == Align.LEFT.align_code
        assert prop.align.align_string == Align.LEFT.align_string
        assert prop.str_len == 8
        assert is_nan(prop.decimal_places)
        assert prop.format_str == "f"

        prop = prop_matrix[3][0]
        assert prop.data == "false"
        assert prop.typecode == Typecode.BOOL
        assert prop.align.align_code == Align.LEFT.align_code
        assert prop.align.align_string == Align.LEFT.align_string
        assert prop.str_len == 5
        assert is_nan(prop.decimal_places)
        assert prop.format_str == ""

        prop = prop_matrix[3][1]
        assert prop.data == "20170101 000000"
        assert prop.typecode == Typecode.DATETIME
        assert prop.align.align_code == Align.LEFT.align_code
        assert prop.align.align_string == Align.LEFT.align_string
        assert prop.str_len == 15
        assert is_nan(prop.decimal_places)
        assert prop.format_str == "s"

    @pytest.mark.parametrize(["value", "expected"], [
        [None, TypeError],
    ])
    def test_exception(self, prop_extractor, value, expected):
        with pytest.raises(expected):
            prop_extractor.data_matrix = value
            prop_extractor.extract_data_property_matrix()

    def test_empty(self, prop_extractor):
        prop_extractor.data_matrix = []
        assert prop_extractor.extract_data_property_matrix() == []


class Test_PropertyExtractor_extract_column_property_list:
    TEST_DATA_MATRIX = [
        [
            1, 1.1,  "aa",   1,   1,     True,   inf,
            nan, datetime.datetime(2017, 1, 1, 0, 0, 0)
        ],
        [
            2, 2.2,  "bbb",  2.2, 2.2,   False,  "inf",
            "nan", "2017-01-01T01:23:45+0900"
        ],
        [
            3, 3.33, "cccc", -3,  "ccc", "true", "infinity",
            "NAN", "2017-11-01 01:23:45+0900"
        ],
    ]

    @pytest.mark.parametrize(["header_list", "value"], [
        [
            ["i", "f", "s", "if", "mix", "bool", "inf", "nan", "time"],
            TEST_DATA_MATRIX,
        ],
        [
            None,
            TEST_DATA_MATRIX,
        ],
        [
            [],
            TEST_DATA_MATRIX,
        ],
    ])
    def test_normal(self, prop_extractor, header_list, value):
        prop_extractor.header_list = header_list
        prop_extractor.data_matrix = value
        col_prop_list = prop_extractor.extract_column_property_list()

        assert len(col_prop_list) == 9

        prop = col_prop_list[0]
        assert prop.typecode == Typecode.INT
        assert prop.align.align_code == Align.RIGHT.align_code
        assert prop.align.align_string == Align.RIGHT.align_string
        assert prop.padding_len == 1
        assert prop.decimal_places == 0
        assert prop.format_str == "d"

        prop = col_prop_list[1]
        assert prop.typecode == Typecode.FLOAT
        assert prop.align.align_code == Align.RIGHT.align_code
        assert prop.align.align_string == Align.RIGHT.align_string
        assert prop.padding_len == 4
        assert prop.decimal_places == 2
        assert prop.format_str == ".2f"

        prop = col_prop_list[2]
        assert prop.typecode == Typecode.STRING
        assert prop.align.align_code == Align.LEFT.align_code
        assert prop.align.align_string == Align.LEFT.align_string
        assert prop.padding_len == 4
        assert is_nan(prop.decimal_places)
        assert prop.format_str == "s"

        prop = col_prop_list[3]
        assert prop.typecode == Typecode.FLOAT
        assert prop.align.align_code == Align.RIGHT.align_code
        assert prop.align.align_string == Align.RIGHT.align_string
        assert prop.padding_len == 4
        assert prop.decimal_places == 1
        assert prop.format_str == ".1f"

        prop = col_prop_list[4]
        assert prop.typecode == Typecode.STRING
        assert prop.align.align_code == Align.LEFT.align_code
        assert prop.align.align_string == Align.LEFT.align_string
        assert prop.padding_len == 3
        assert prop.decimal_places == 1
        assert prop.format_str == "s"

        prop = col_prop_list[5]
        assert prop.typecode == Typecode.BOOL
        assert prop.align.align_code == Align.LEFT.align_code
        assert prop.align.align_string == Align.LEFT.align_string
        assert prop.padding_len == 5
        assert is_nan(prop.decimal_places)
        assert prop.format_str == ""

        prop = col_prop_list[6]
        assert prop.typecode == Typecode.INFINITY
        assert prop.align.align_code == Align.LEFT.align_code
        assert prop.align.align_string == Align.LEFT.align_string
        assert prop.padding_len == 3
        assert is_nan(prop.decimal_places)
        assert prop.format_str == "f"

        prop = col_prop_list[7]
        assert prop.typecode == Typecode.NAN
        assert prop.align.align_code == Align.LEFT.align_code
        assert prop.align.align_string == Align.LEFT.align_string
        assert prop.padding_len == 3
        assert is_nan(prop.decimal_places)
        assert prop.format_str == "f"

        prop = col_prop_list[8]
        assert prop.typecode == Typecode.DATETIME
        assert prop.align.align_code == Align.LEFT.align_code
        assert prop.align.align_string == Align.LEFT.align_string
        assert prop.padding_len == 24
        assert is_nan(prop.decimal_places)
        assert prop.format_str == "%Y-%m-%dT%H:%M:%S%z"

    def test_normal_empty_value(self, prop_extractor):
        prop_extractor.header_list = ["a", "22", "cccc"]
        prop_extractor.data_matrix = None
        col_prop_list = prop_extractor.extract_column_property_list()

        prop = col_prop_list[0]
        assert prop.typecode == Typecode.NONE
        assert prop.align.align_code == Align.LEFT.align_code
        assert prop.align.align_string == Align.LEFT.align_string
        assert prop.padding_len == 1
        assert is_nan(prop.decimal_places)
        assert prop.format_str == ""

        prop = col_prop_list[1]
        assert prop.typecode == Typecode.NONE
        assert prop.align.align_code == Align.LEFT.align_code
        assert prop.align.align_string == Align.LEFT.align_string
        assert prop.padding_len == 2
        assert is_nan(prop.decimal_places)
        assert prop.format_str == ""

        prop = col_prop_list[2]
        assert prop.typecode == Typecode.NONE
        assert prop.align.align_code == Align.LEFT.align_code
        assert prop.align.align_string == Align.LEFT.align_string
        assert prop.padding_len == 4
        assert is_nan(prop.decimal_places)
        assert prop.format_str == ""
