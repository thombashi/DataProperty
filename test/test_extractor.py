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
def dp_extractor():
    return DataPropertyExtractor()


def bool_converter_test(value):
    return str(value).lower()


def datetime_converter_test(value):
    return value.strftime("%Y%m%d %H%M%S")


class Test_DataPropertyExtractor_to_dataproperty_matrix:

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
    def test_smoke(self, dp_extractor, value):
        dp_extractor.data_matrix = value

        assert len(dp_extractor.to_dataproperty_matrix()) > 0

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
            self, dp_extractor, value, none_value, inf_value, nan_value,
            bool_converter, datetime_converter):
        dp_extractor.data_matrix = value
        dp_extractor.none_value = none_value
        dp_extractor.inf_value = inf_value
        dp_extractor.nan_value = nan_value
        dp_extractor.bool_converter = bool_converter_test
        dp_extractor.datetime_converter = datetime_converter
        dp_extractor.datetime_format_str = "s"
        dp_matrix = dp_extractor.to_dataproperty_matrix()

        assert len(dp_matrix) == 4

        dp = dp_matrix[0][0]
        assert dp.data == "null"
        assert dp.typecode == Typecode.NONE
        assert dp.align.align_code == Align.LEFT.align_code
        assert dp.align.align_string == Align.LEFT.align_string
        assert dp.str_len == 4
        assert NanType(dp.decimal_places).is_type()
        assert dp.format_str == ""

        dp = dp_matrix[0][1]
        assert dp.data == 1
        assert dp.typecode == Typecode.INTEGER
        assert dp.align.align_code == Align.RIGHT.align_code
        assert dp.align.align_string == Align.RIGHT.align_string
        assert dp.str_len == 1
        assert dp.decimal_places == 0
        assert dp.format_str == "d"

        dp = dp_matrix[1][0]
        assert dp.data == Decimal("1.1")
        assert dp.typecode == Typecode.FLOAT
        assert dp.align.align_code == Align.RIGHT.align_code
        assert dp.align.align_string == Align.RIGHT.align_string
        assert dp.str_len == 3
        assert dp.decimal_places == 1
        assert dp.format_str == ".1f"

        dp = dp_matrix[1][1]
        assert dp.data == "a"
        assert dp.typecode == Typecode.STRING
        assert dp.align.align_code == Align.LEFT.align_code
        assert dp.align.align_string == Align.LEFT.align_string
        assert dp.str_len == 1
        assert NanType(dp.decimal_places).is_type()
        assert dp.format_str == "s"

        dp = dp_matrix[2][0]
        assert dp.data == "NaN"
        assert dp.typecode == Typecode.NAN
        assert dp.align.align_code == Align.LEFT.align_code
        assert dp.align.align_string == Align.LEFT.align_string
        assert dp.str_len == 3
        assert NanType(dp.decimal_places).is_type()
        assert dp.format_str == "f"

        dp = dp_matrix[2][1]
        assert dp.data == "Infinity"
        assert dp.typecode == Typecode.INFINITY
        assert dp.align.align_code == Align.LEFT.align_code
        assert dp.align.align_string == Align.LEFT.align_string
        assert dp.str_len == 8
        assert NanType(dp.decimal_places).is_type()
        assert dp.format_str == "f"

        dp = dp_matrix[3][0]
        assert dp.data == "false"
        assert dp.typecode == Typecode.BOOL
        assert dp.align.align_code == Align.LEFT.align_code
        assert dp.align.align_string == Align.LEFT.align_string
        assert dp.str_len == 5
        assert NanType(dp.decimal_places).is_type()
        assert dp.format_str == ""

        dp = dp_matrix[3][1]
        assert dp.data == "20170101 000000"
        assert dp.typecode == Typecode.DATETIME
        assert dp.align.align_code == Align.LEFT.align_code
        assert dp.align.align_string == Align.LEFT.align_string
        assert dp.str_len == 15
        assert NanType(dp.decimal_places).is_type()
        assert dp.format_str == "s"

    @pytest.mark.parametrize(["value", "expected"], [
        [None, TypeError],
    ])
    def test_exception(self, dp_extractor, value, expected):
        with pytest.raises(expected):
            dp_extractor.data_matrix = value
            dp_extractor.to_dataproperty_matrix()

    def test_empty(self, dp_extractor):
        dp_extractor.data_matrix = []
        assert dp_extractor.to_dataproperty_matrix() == []


class Test_DataPropertyExtractor_to_dataproperty_list:

    @pytest.mark.parametrize(["value", "float_type"], [
        [[0.1, Decimal("1.1")], float],
        [[0.1, Decimal("1.1")], Decimal],
    ])
    def test_normal_float(self, dp_extractor, value, float_type):
        dp_extractor.float_type = float_type
        dp_list = dp_extractor.to_dataproperty_list(value)

        for dp in dp_list:
            assert isinstance(dp.data, float_type)

    @pytest.mark.parametrize(["value", "strip_str", "expected"], [
        [
            ['"1"', '"-1.1"', '"abc"'],
            '"',
            [1, Decimal("-1.1"), "abc"],
        ],
    ])
    def test_normal_strip_str(
            self, dp_extractor, value, strip_str, expected):
        dp_extractor.strip_str = strip_str
        dp_list = dp_extractor.to_dataproperty_list(value)

        for dp, value in zip(dp_list, expected):
            assert dp.data == value


class Test_DataPropertyExtractor_to_col_dataproperty_list:
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
    def test_normal_default(self, dp_extractor, header_list, value):
        dp_extractor.header_list = header_list
        dp_extractor.data_matrix = value
        col_dp_list = dp_extractor.to_col_dataproperty_list()

        assert len(col_dp_list) == 9

        dp = col_dp_list[0]
        assert dp.typecode == Typecode.INTEGER
        assert dp.align.align_code == Align.RIGHT.align_code
        assert dp.align.align_string == Align.RIGHT.align_string
        assert dp.ascii_char_width == 1
        assert dp.decimal_places == 0
        assert dp.format_str == "d"

        dp = col_dp_list[1]
        assert dp.typecode == Typecode.FLOAT
        assert dp.align.align_code == Align.RIGHT.align_code
        assert dp.align.align_string == Align.RIGHT.align_string
        assert dp.ascii_char_width == 4
        assert dp.decimal_places == 2
        assert dp.format_str == ".2f"

        dp = col_dp_list[2]
        assert dp.typecode == Typecode.STRING
        assert dp.align.align_code == Align.LEFT.align_code
        assert dp.align.align_string == Align.LEFT.align_string
        assert dp.ascii_char_width == 4
        assert NanType(dp.decimal_places).is_type()
        assert dp.format_str == "s"

        dp = col_dp_list[3]
        assert dp.typecode == Typecode.FLOAT
        assert dp.align.align_code == Align.RIGHT.align_code
        assert dp.align.align_string == Align.RIGHT.align_string
        assert dp.ascii_char_width == 4
        assert dp.decimal_places == 1
        assert dp.format_str == ".1f"

        dp = col_dp_list[4]
        assert dp.typecode == Typecode.STRING
        assert dp.align.align_code == Align.LEFT.align_code
        assert dp.align.align_string == Align.LEFT.align_string
        assert dp.ascii_char_width == 3
        assert dp.decimal_places == 1
        assert dp.format_str == "s"

        dp = col_dp_list[5]
        assert dp.typecode == Typecode.BOOL
        assert dp.align.align_code == Align.LEFT.align_code
        assert dp.align.align_string == Align.LEFT.align_string
        assert dp.ascii_char_width == 5
        assert NanType(dp.decimal_places).is_type()
        assert dp.format_str == ""

        dp = col_dp_list[6]
        assert dp.typecode == Typecode.INFINITY
        assert dp.align.align_code == Align.LEFT.align_code
        assert dp.align.align_string == Align.LEFT.align_string
        assert dp.ascii_char_width == 8
        assert NanType(dp.decimal_places).is_type()
        assert dp.format_str == "f"

        dp = col_dp_list[7]
        assert dp.typecode == Typecode.NAN
        assert dp.align.align_code == Align.LEFT.align_code
        assert dp.align.align_string == Align.LEFT.align_string
        assert dp.ascii_char_width == 3
        assert NanType(dp.decimal_places).is_type()
        assert dp.format_str == "f"

        dp = col_dp_list[8]
        assert dp.typecode == Typecode.STRING
        assert dp.align.align_code == Align.LEFT.align_code
        assert dp.align.align_string == Align.LEFT.align_string
        assert dp.ascii_char_width == 24
        assert NanType(dp.decimal_places).is_type()
        assert dp.format_str == "s"

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
    def test_normal_not_strict(self, dp_extractor, header_list, value):
        dp_extractor.header_list = header_list
        dp_extractor.data_matrix = value
        dp_extractor.strict_type_mapping = NOT_STRICT_TYPE_MAPPING
        col_dp_list = dp_extractor.to_col_dataproperty_list()

        assert len(col_dp_list) == 9

        dp = col_dp_list[0]
        assert dp.typecode == Typecode.INTEGER
        assert dp.align.align_code == Align.RIGHT.align_code
        assert dp.align.align_string == Align.RIGHT.align_string
        assert dp.ascii_char_width == 1
        assert dp.decimal_places == 0
        assert dp.format_str == "d"

        dp = col_dp_list[1]
        assert dp.typecode == Typecode.FLOAT
        assert dp.align.align_code == Align.RIGHT.align_code
        assert dp.align.align_string == Align.RIGHT.align_string
        assert dp.ascii_char_width == 4
        assert dp.decimal_places == 2
        assert dp.format_str == ".2f"

    def test_normal_nan_inf(self, dp_extractor):
        dp_extractor.header_list = ["n", "i"]
        dp_extractor.data_matrix = [
            [nan, inf],
            ["nan", "inf"],
        ]
        col_dp_list = dp_extractor.to_col_dataproperty_list()

        assert len(col_dp_list) == 2

        dp = col_dp_list[0]
        assert dp.typecode == Typecode.NAN
        assert dp.align.align_code == Align.LEFT.align_code
        assert dp.align.align_string == Align.LEFT.align_string
        assert dp.ascii_char_width == 3
        assert NanType(dp.decimal_places).is_type()

        dp = col_dp_list[1]
        assert dp.typecode == Typecode.INFINITY
        assert dp.align.align_code == Align.LEFT.align_code
        assert dp.align.align_string == Align.LEFT.align_string
        assert dp.ascii_char_width == 8
        assert NanType(dp.decimal_places).is_type()

    @pytest.mark.parametrize(["ambiguous_width"], [
        [2],
        [1],
    ])
    def test_normal_east_asian_ambiguous_width(
            self, dp_extractor, ambiguous_width):
        dp_extractor.header_list = ["ascii", "eaa"]
        dp_extractor.data_matrix = [
            ["abcdefg", "Øαββ"],
            ["abcdefghij", "ØØ"],
        ]
        dp_extractor.east_asian_ambiguous_width = ambiguous_width
        col_dp_list = dp_extractor.to_col_dataproperty_list()

        assert len(col_dp_list) == 2

        dp = col_dp_list[0]
        assert dp.typecode == Typecode.STRING
        assert dp.align.align_code == Align.LEFT.align_code
        assert dp.align.align_string == Align.LEFT.align_string
        assert dp.ascii_char_width == 10
        assert NanType(dp.decimal_places).is_type()

        dp = col_dp_list[1]
        assert dp.typecode == Typecode.STRING
        assert dp.align.align_code == Align.LEFT.align_code
        assert dp.align.align_string == Align.LEFT.align_string
        assert dp.ascii_char_width == 4 * ambiguous_width
        assert NanType(dp.decimal_places).is_type()

    def test_normal_empty_value(self, dp_extractor):
        dp_extractor.header_list = ["a", "22", "cccc"]
        dp_extractor.data_matrix = None
        col_dp_list = dp_extractor.to_col_dataproperty_list()

        dp = col_dp_list[0]
        assert dp.typecode == Typecode.NONE
        assert dp.align.align_code == Align.LEFT.align_code
        assert dp.align.align_string == Align.LEFT.align_string
        assert dp.ascii_char_width == 1
        assert NanType(dp.decimal_places).is_type()
        assert dp.format_str == ""

        dp = col_dp_list[1]
        assert dp.typecode == Typecode.NONE
        assert dp.align.align_code == Align.LEFT.align_code
        assert dp.align.align_string == Align.LEFT.align_string
        assert dp.ascii_char_width == 2
        assert NanType(dp.decimal_places).is_type()
        assert dp.format_str == ""

        dp = col_dp_list[2]
        assert dp.typecode == Typecode.NONE
        assert dp.align.align_code == Align.LEFT.align_code
        assert dp.align.align_string == Align.LEFT.align_string
        assert dp.ascii_char_width == 4
        assert NanType(dp.decimal_places).is_type()
        assert dp.format_str == ""

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
            self, dp_extractor, header_list, value, mismatch_processing,
            expected):
        dp_extractor.header_list = header_list
        dp_extractor.data_matrix = value
        dp_extractor.mismatch_processing = mismatch_processing
        col_dp_list = dp_extractor.to_col_dataproperty_list()

        assert len(col_dp_list) == expected

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
            self, dp_extractor, header_list, value, mismatch_processing,
            expected):
        dp_extractor.header_list = header_list
        dp_extractor.data_matrix = value
        dp_extractor.mismatch_processing = mismatch_processing

        with pytest.raises(expected):
            dp_extractor.to_col_dataproperty_list()
