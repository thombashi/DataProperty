# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <gogogo.vm@gmail.com>
"""

from __future__ import unicode_literals
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

    @pytest.mark.parametrize(["value"], [
        [
            [
                ["山田", "太郎", "2001/1/1", "100-0002",
                             "東京都千代田区皇居外苑", "03-1234-5678"],
                ["山田", "次郎", "2001/1/2", "251-0036",
                             "神奈川県藤沢市江の島１丁目", "03-9999-9999"],
            ],
        ],
    ])
    def test_smoke(self, prop_extractor, value):
        prop_extractor.data_matrix = value

        assert len(prop_extractor.extract_data_property_matrix()) > 0

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
        ]
    )
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
        assert NanType(prop.decimal_places).is_type()
        assert prop.format_str == ""

        prop = prop_matrix[0][1]
        assert prop.data == 1
        assert prop.typecode == Typecode.INTEGER
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
        assert NanType(prop.decimal_places).is_type()
        assert prop.format_str == "s"

        prop = prop_matrix[2][0]
        assert prop.data == "NaN"
        assert prop.typecode == Typecode.NAN
        assert prop.align.align_code == Align.LEFT.align_code
        assert prop.align.align_string == Align.LEFT.align_string
        assert prop.str_len == 3
        assert NanType(prop.decimal_places).is_type()
        assert prop.format_str == "f"

        prop = prop_matrix[2][1]
        assert prop.data == "Infinity"
        assert prop.typecode == Typecode.INFINITY
        assert prop.align.align_code == Align.LEFT.align_code
        assert prop.align.align_string == Align.LEFT.align_string
        assert prop.str_len == 8
        assert NanType(prop.decimal_places).is_type()
        assert prop.format_str == "f"

        prop = prop_matrix[3][0]
        assert prop.data == "false"
        assert prop.typecode == Typecode.BOOL
        assert prop.align.align_code == Align.LEFT.align_code
        assert prop.align.align_string == Align.LEFT.align_string
        assert prop.str_len == 5
        assert NanType(prop.decimal_places).is_type()
        assert prop.format_str == ""

        prop = prop_matrix[3][1]
        assert prop.data == "20170101 000000"
        assert prop.typecode == Typecode.DATETIME
        assert prop.align.align_code == Align.LEFT.align_code
        assert prop.align.align_string == Align.LEFT.align_string
        assert prop.str_len == 15
        assert NanType(prop.decimal_places).is_type()
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


class Test_PropertyExtractor_extract_data_property_list:

    @pytest.mark.parametrize(["value", "float_type"], [
        [[0.1, Decimal("1.1")], float],
        [[0.1, Decimal("1.1")], Decimal],
    ])
    def test_normal_float(self, prop_extractor, value, float_type):
        prop_extractor.float_type = float_type
        prop_list = prop_extractor.extract_data_property_list(value)

        for prop in prop_list:
            assert isinstance(prop.data, float_type)


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
    def test_normal_default(self, prop_extractor, header_list, value):
        prop_extractor.header_list = header_list
        prop_extractor.data_matrix = value
        col_prop_list = prop_extractor.extract_col_property_list()

        assert len(col_prop_list) == 9

        prop = col_prop_list[0]
        assert prop.typecode == Typecode.INTEGER
        assert prop.align.align_code == Align.RIGHT.align_code
        assert prop.align.align_string == Align.RIGHT.align_string
        assert prop.ascii_char_width == 1
        assert prop.decimal_places == 0
        assert prop.format_str == "d"

        prop = col_prop_list[1]
        assert prop.typecode == Typecode.FLOAT
        assert prop.align.align_code == Align.RIGHT.align_code
        assert prop.align.align_string == Align.RIGHT.align_string
        assert prop.ascii_char_width == 4
        assert prop.decimal_places == 2
        assert prop.format_str == ".2f"

        prop = col_prop_list[2]
        assert prop.typecode == Typecode.STRING
        assert prop.align.align_code == Align.LEFT.align_code
        assert prop.align.align_string == Align.LEFT.align_string
        assert prop.ascii_char_width == 4
        assert NanType(prop.decimal_places).is_type()
        assert prop.format_str == "s"

        prop = col_prop_list[3]
        assert prop.typecode == Typecode.FLOAT
        assert prop.align.align_code == Align.RIGHT.align_code
        assert prop.align.align_string == Align.RIGHT.align_string
        assert prop.ascii_char_width == 4
        assert prop.decimal_places == 1
        assert prop.format_str == ".1f"

        prop = col_prop_list[4]
        assert prop.typecode == Typecode.STRING
        assert prop.align.align_code == Align.LEFT.align_code
        assert prop.align.align_string == Align.LEFT.align_string
        assert prop.ascii_char_width == 3
        assert prop.decimal_places == 1
        assert prop.format_str == "s"

        prop = col_prop_list[5]
        assert prop.typecode == Typecode.BOOL
        assert prop.align.align_code == Align.LEFT.align_code
        assert prop.align.align_string == Align.LEFT.align_string
        assert prop.ascii_char_width == 5
        assert NanType(prop.decimal_places).is_type()
        assert prop.format_str == ""

        prop = col_prop_list[6]
        assert prop.typecode == Typecode.INFINITY
        assert prop.align.align_code == Align.LEFT.align_code
        assert prop.align.align_string == Align.LEFT.align_string
        assert prop.ascii_char_width == 8
        assert NanType(prop.decimal_places).is_type()
        assert prop.format_str == "f"

        prop = col_prop_list[7]
        assert prop.typecode == Typecode.NAN
        assert prop.align.align_code == Align.LEFT.align_code
        assert prop.align.align_string == Align.LEFT.align_string
        assert prop.ascii_char_width == 3
        assert NanType(prop.decimal_places).is_type()
        assert prop.format_str == "f"

        prop = col_prop_list[8]
        assert prop.typecode == Typecode.STRING
        assert prop.align.align_code == Align.LEFT.align_code
        assert prop.align.align_string == Align.LEFT.align_string
        assert prop.ascii_char_width == 24
        assert NanType(prop.decimal_places).is_type()
        assert prop.format_str == "s"

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
    def test_normal_not_strict(self, prop_extractor, header_list, value):
        prop_extractor.header_list = header_list
        prop_extractor.data_matrix = value
        prop_extractor.strict_type_mapping = NOT_STRICT_TYPE_MAPPING
        col_prop_list = prop_extractor.extract_col_property_list()

        assert len(col_prop_list) == 9

        prop = col_prop_list[0]
        assert prop.typecode == Typecode.INTEGER
        assert prop.align.align_code == Align.RIGHT.align_code
        assert prop.align.align_string == Align.RIGHT.align_string
        assert prop.ascii_char_width == 1
        assert prop.decimal_places == 0
        assert prop.format_str == "d"

        prop = col_prop_list[1]
        assert prop.typecode == Typecode.FLOAT
        assert prop.align.align_code == Align.RIGHT.align_code
        assert prop.align.align_string == Align.RIGHT.align_string
        assert prop.ascii_char_width == 4
        assert prop.decimal_places == 2
        assert prop.format_str == ".2f"

    def test_normal_nan_inf(self, prop_extractor):
        prop_extractor.header_list = ["n", "i"]
        prop_extractor.data_matrix = [
            [nan, inf],
            ["nan", "inf"],
        ]
        col_prop_list = prop_extractor.extract_col_property_list()

        assert len(col_prop_list) == 2

        prop = col_prop_list[0]
        assert prop.typecode == Typecode.NAN
        assert prop.align.align_code == Align.LEFT.align_code
        assert prop.align.align_string == Align.LEFT.align_string
        assert prop.ascii_char_width == 3
        assert NanType(prop.decimal_places).is_type()

        prop = col_prop_list[1]
        assert prop.typecode == Typecode.INFINITY
        assert prop.align.align_code == Align.LEFT.align_code
        assert prop.align.align_string == Align.LEFT.align_string
        assert prop.ascii_char_width == 8
        assert NanType(prop.decimal_places).is_type()

    @pytest.mark.parametrize(["ambiguous_width"], [
        [2],
        [1],
    ])
    def test_normal_east_asian_ambiguous_width(
            self, prop_extractor, ambiguous_width):
        prop_extractor.header_list = ["ascii", "eaa"]
        prop_extractor.data_matrix = [
            ["abcdefg", "Øαββ"],
            ["abcdefghij", "ØØ"],
        ]
        prop_extractor.east_asian_ambiguous_width = ambiguous_width
        col_prop_list = prop_extractor.extract_col_property_list()

        assert len(col_prop_list) == 2

        prop = col_prop_list[0]
        assert prop.typecode == Typecode.STRING
        assert prop.align.align_code == Align.LEFT.align_code
        assert prop.align.align_string == Align.LEFT.align_string
        assert prop.ascii_char_width == 10
        assert NanType(prop.decimal_places).is_type()

        prop = col_prop_list[1]
        assert prop.typecode == Typecode.STRING
        assert prop.align.align_code == Align.LEFT.align_code
        assert prop.align.align_string == Align.LEFT.align_string
        assert prop.ascii_char_width == 4 * ambiguous_width
        assert NanType(prop.decimal_places).is_type()

    def test_normal_empty_value(self, prop_extractor):
        prop_extractor.header_list = ["a", "22", "cccc"]
        prop_extractor.data_matrix = None
        col_prop_list = prop_extractor.extract_col_property_list()

        prop = col_prop_list[0]
        assert prop.typecode == Typecode.NONE
        assert prop.align.align_code == Align.LEFT.align_code
        assert prop.align.align_string == Align.LEFT.align_string
        assert prop.ascii_char_width == 1
        assert NanType(prop.decimal_places).is_type()
        assert prop.format_str == ""

        prop = col_prop_list[1]
        assert prop.typecode == Typecode.NONE
        assert prop.align.align_code == Align.LEFT.align_code
        assert prop.align.align_string == Align.LEFT.align_string
        assert prop.ascii_char_width == 2
        assert NanType(prop.decimal_places).is_type()
        assert prop.format_str == ""

        prop = col_prop_list[2]
        assert prop.typecode == Typecode.NONE
        assert prop.align.align_code == Align.LEFT.align_code
        assert prop.align.align_string == Align.LEFT.align_string
        assert prop.ascii_char_width == 4
        assert NanType(prop.decimal_places).is_type()
        assert prop.format_str == ""

    @pytest.mark.parametrize(
        ["header_list", "value", "mismatch_processing", "expected"],
        [
            [
                ["i", "f", "s", "if", "mix"],
                TEST_DATA_MATRIX,
                MissmatchProcessing.TRIM,
                5,
            ],
            [
                None,
                TEST_DATA_MATRIX,
                MissmatchProcessing.EXTEND,
                9
            ],
        ])
    def test_normal_mismatch_processing(
            self, prop_extractor, header_list, value, mismatch_processing,
            expected):
        prop_extractor.header_list = header_list
        prop_extractor.data_matrix = value
        prop_extractor.mismatch_processing = mismatch_processing
        col_prop_list = prop_extractor.extract_col_property_list()

        assert len(col_prop_list) == expected

    @pytest.mark.parametrize(
        ["header_list", "value", "mismatch_processing", "expected"],
        [
            [
                ["i", "f", "s", "if", "mix"],
                TEST_DATA_MATRIX,
                MissmatchProcessing.EXCEPTION,
                ValueError,
            ],
        ])
    def test_exception_mismatch_processing(
            self, prop_extractor, header_list, value, mismatch_processing,
            expected):
        prop_extractor.header_list = header_list
        prop_extractor.data_matrix = value
        prop_extractor.mismatch_processing = mismatch_processing

        with pytest.raises(expected):
            prop_extractor.extract_col_property_list()
