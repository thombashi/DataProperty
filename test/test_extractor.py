# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

from __future__ import unicode_literals

import datetime
from decimal import Decimal

import pytest
import six
from dataproperty import Align, DataPropertyExtractor, MatrixFormatting
from six import text_type
from typepy import DateTime, RealNumber, String, Typecode

from .common import get_strict_type_mapping


DATATIME_DATA = datetime.datetime(2017, 1, 2, 3, 4, 5)

nan = float("nan")
inf = float("inf")


@pytest.fixture
def dp_extractor():
    return DataPropertyExtractor()


def datetime_formatter_test(value):
    return value.strftime("%Y%m%d %H%M%S")


def datetime_formatter_tostr_0(value):
    return value.strftime("%Y-%m-%d %H:%M:%S%z")


def datetime_formatter_tostr_1(value):
    return value.strftime("%Y/%m/%d %H:%M:%S")


class Test_DataPropertyExtractor_to_dp(object):
    @pytest.mark.parametrize(
        ["value", "type_value_mapping", "is_strict", "expected_value", "expected_typecode"],
        [
            [None, {Typecode.NONE: None}, True, None, Typecode.NONE],
            [None, {Typecode.NONE: "null"}, False, "null", Typecode.STRING],
            [None, {Typecode.NONE: ""}, True, "", Typecode.NULL_STRING],
            [None, {Typecode.NONE: 0}, False, 0, Typecode.INTEGER],
            [inf, {Typecode.INFINITY: "INF_1"}, False, "INF_1", Typecode.STRING],
            [inf, {Typecode.INFINITY: "INF_2"}, True, "INF_2", Typecode.STRING],
            [inf, {Typecode.INFINITY: None}, True, None, Typecode.NONE],
            ["inf", {Typecode.INFINITY: "INF_3"}, False, "INF_3", Typecode.STRING],
            ["inf", {Typecode.INFINITY: "INF_4"}, True, "inf", Typecode.STRING],
            ["inf", {Typecode.INFINITY: inf}, False, Decimal("Infinity"), Typecode.INFINITY],
            [nan, {Typecode.NAN: "NAN_1"}, False, "NAN_1", Typecode.STRING],
            [nan, {Typecode.NAN: "NAN_2"}, True, "NAN_2", Typecode.STRING],
            [nan, {Typecode.NAN: None}, True, None, Typecode.NONE],
            ["nan", {Typecode.NAN: "NAN_4"}, False, "NAN_4", Typecode.STRING],
            ["nan", {Typecode.NAN: "NAN_5"}, True, "nan", Typecode.STRING],
        ],
    )
    def test_normal_type_value_mapping(
        self, dp_extractor, value, type_value_mapping, is_strict, expected_value, expected_typecode
    ):
        dp_extractor.type_value_mapping = type_value_mapping
        dp_extractor.strict_type_mapping = get_strict_type_mapping(is_strict)
        dp = dp_extractor.to_dp(value)

        assert dp.data == expected_value
        assert dp.typecode == expected_typecode
        assert isinstance(dp.to_str(), six.text_type)

    @pytest.mark.parametrize(
        ["value", "datetime_formatter", "datetime_format_str", "is_strict", "expected"],
        [
            [DATATIME_DATA, datetime_formatter_tostr_0, "s", False, "2017-01-02 03:04:05"],
            ["2017-01-01 00:00:00", datetime_formatter_tostr_1, "s", False, "2017/01/01 00:00:00"],
            [
                "2017-01-01 00:00:00",
                None,
                "%Y-%m-%dT%H:%M:%S",
                False,
                datetime.datetime(2017, 1, 1, 0, 0, 0),
            ],
            ["2017-01-01 00:00:00", None, "s", True, "2017-01-01 00:00:00"],
        ],
    )
    def test_normal_datetime(
        self, dp_extractor, value, datetime_formatter, datetime_format_str, is_strict, expected
    ):
        dp_extractor.datetime_formatter = datetime_formatter
        dp_extractor.datetime_format_str = datetime_format_str
        dp_extractor.strict_type_mapping = get_strict_type_mapping(is_strict)
        dp = dp_extractor.to_dp(value)

        assert dp.data == expected


class Test_DataPropertyExtractor_to_dp_quoting_flags(object):
    ALWAYS_QUOTE_FLAG_MAPPING = {
        Typecode.NONE: True,
        Typecode.INTEGER: True,
        Typecode.REAL_NUMBER: True,
        Typecode.STRING: True,
        Typecode.NULL_STRING: True,
        Typecode.DATETIME: True,
        Typecode.REAL_NUMBER: True,
        Typecode.NAN: True,
        Typecode.BOOL: True,
    }

    @pytest.mark.parametrize(
        ["value", "quoting_flags", "is_strict", "expected"],
        [
            ["string", ALWAYS_QUOTE_FLAG_MAPPING, False, '"string"'],
            ['"string"', ALWAYS_QUOTE_FLAG_MAPPING, False, '"string"'],
            [' "123"', ALWAYS_QUOTE_FLAG_MAPPING, False, ' "123"'],
            ['"string" ', ALWAYS_QUOTE_FLAG_MAPPING, False, '"string" '],
            [' "12 345" ', ALWAYS_QUOTE_FLAG_MAPPING, False, ' "12 345" '],
        ],
    )
    def test_normal_always_quote(self, dp_extractor, value, quoting_flags, is_strict, expected):
        dp_extractor.quoting_flags = quoting_flags
        dp = dp_extractor.to_dp(value)

        assert dp.data == expected


class Test_DataPropertyExtractor_to_dp_const_value_mapping(object):
    VALUE_MAPPING = {True: "true value", False: "false value", "const": "const value"}

    @pytest.mark.parametrize(
        ["value", "const_value_mapping", "is_strict", "expected"],
        [
            ["True", VALUE_MAPPING, False, "true value"],
            ["False", VALUE_MAPPING, False, "false value"],
            ["True", VALUE_MAPPING, True, "True"],
            [True, VALUE_MAPPING, True, "true value"],
            ["const", VALUE_MAPPING, True, "const value"],
        ],
    )
    def test_normal(self, dp_extractor, value, const_value_mapping, is_strict, expected):
        dp_extractor.const_value_mapping = const_value_mapping
        dp_extractor.strict_type_mapping = get_strict_type_mapping(is_strict)
        dp = dp_extractor.to_dp(value)

        assert dp.data == expected


class Test_DataPropertyExtractor_to_dp_matrix(object):
    @pytest.mark.parametrize(
        ["value"],
        [
            [
                [
                    ["山田", "太郎", "2001/1/1", "100-0002", "東京都千代田区皇居外苑", "03-1234-5678"],
                    ["山田", "次郎", "2001/1/2", "251-0036", "神奈川県藤沢市江の島１丁目", "03-9999-9999"],
                ]
            ]
        ],
    )
    def test_smoke(self, dp_extractor, value):
        assert len(list(dp_extractor.to_dp_matrix(value))) > 0

    @pytest.mark.parametrize(
        ["value", "type_value_mapping", "const_value_mapping", "datetime_formatter"],
        [
            [
                [[None, "1"], [1.1, "a"], [nan, inf], ["false", DATATIME_DATA]],
                {Typecode.NONE: "null", Typecode.INFINITY: "INFINITY", Typecode.NAN: "NAN"},
                {True: "true", False: "false"},
                datetime_formatter_test,
            ]
        ],
    )
    def test_normal(
        self, dp_extractor, value, type_value_mapping, const_value_mapping, datetime_formatter
    ):
        dp_extractor.type_value_mapping = type_value_mapping
        dp_extractor.const_value_mapping = const_value_mapping
        dp_extractor.datetime_formatter = datetime_formatter
        dp_matrix = list(dp_extractor.to_dp_matrix(dp_extractor.to_dp_matrix(value)))

        assert len(dp_matrix) == 4

        dp = dp_matrix[0][0]
        assert dp.data == "null"
        assert dp.typecode == Typecode.STRING
        assert dp.align.align_code == Align.LEFT.align_code
        assert dp.align.align_string == Align.LEFT.align_string
        assert dp.decimal_places is None
        assert dp.format_str == "{:s}"

        dp = dp_matrix[0][1]
        assert dp.data == 1
        assert dp.typecode == Typecode.INTEGER
        assert dp.align.align_code == Align.RIGHT.align_code
        assert dp.align.align_string == Align.RIGHT.align_string
        assert dp.decimal_places == 0
        assert dp.format_str == "{:d}"

        dp = dp_matrix[1][0]
        assert dp.data == Decimal("1.1")
        assert dp.typecode == Typecode.REAL_NUMBER
        assert dp.align.align_code == Align.RIGHT.align_code
        assert dp.align.align_string == Align.RIGHT.align_string
        assert dp.decimal_places == 1
        assert dp.format_str == "{:.1f}"

        dp = dp_matrix[1][1]
        assert dp.data == "a"
        assert dp.typecode == Typecode.STRING
        assert dp.align.align_code == Align.LEFT.align_code
        assert dp.align.align_string == Align.LEFT.align_string
        assert dp.decimal_places is None
        assert dp.format_str == "{:s}"

        dp = dp_matrix[2][0]
        assert dp.data == "NAN"
        assert dp.typecode == Typecode.STRING
        assert dp.align.align_code == Align.LEFT.align_code
        assert dp.align.align_string == Align.LEFT.align_string
        assert dp.decimal_places is None
        assert dp.format_str == "{:s}"

        dp = dp_matrix[2][1]
        assert dp.data == "INFINITY"
        assert dp.typecode == Typecode.STRING
        assert dp.align.align_code == Align.LEFT.align_code
        assert dp.align.align_string == Align.LEFT.align_string
        assert dp.decimal_places is None
        assert dp.format_str == "{:s}"

        dp = dp_matrix[3][0]
        assert dp.data == "false"
        assert dp.typecode == Typecode.STRING
        assert dp.align.align_code == Align.LEFT.align_code
        assert dp.align.align_string == Align.LEFT.align_string
        assert dp.decimal_places is None
        assert dp.format_str == "{:s}"

        dp = dp_matrix[3][1]
        assert dp.data == "20170102 030405"
        assert dp.typecode == Typecode.STRING
        assert dp.align.align_code == Align.LEFT.align_code
        assert dp.align.align_string == Align.LEFT.align_string
        assert dp.decimal_places is None
        assert dp.format_str == "{:s}"

    @pytest.mark.parametrize(["value", "expected"], [[None, []], [[], []], [(), []]])
    def test_empty(self, dp_extractor, value, expected):
        assert dp_extractor.to_dp_matrix(value) == expected


class Test_DataPropertyExtractor_to_dp_list(object):
    @pytest.mark.parametrize(
        ["value", "float_type"], [[[0.1, Decimal("1.1")], float], [[0.1, Decimal("1.1")], Decimal]]
    )
    def test_normal_float(self, dp_extractor, value, float_type):
        dp_extractor.float_type = float_type
        dp_list = dp_extractor.to_dp_list(value)

        for dp in dp_list:
            assert isinstance(dp.data, float_type)

    @pytest.mark.parametrize(
        ["value", "type_hint", "expected_list"],
        [
            [
                ["2017-01-02 03:04:05", datetime.datetime(2017, 1, 2, 3, 4, 5)],
                None,
                [Typecode.STRING, Typecode.DATETIME],
            ],
            [
                ["2017-01-02 03:04:05", datetime.datetime(2017, 1, 2, 3, 4, 5)],
                DateTime,
                [Typecode.DATETIME, Typecode.DATETIME],
            ],
        ],
    )
    def test_normal_type_hint(self, dp_extractor, value, type_hint, expected_list):
        dp_extractor.default_type_hint = type_hint
        dp_list = dp_extractor.to_dp_list(value)

        for dp, expected in zip(dp_list, expected_list):
            assert dp.typecode == expected

    @pytest.mark.parametrize(
        ["value", "strip_str_header", "strip_str_value", "expected"],
        [
            [['"1"', '"-1.1"', '"abc"'], "", '"', [1, Decimal("-1.1"), "abc"]],
            [['"1"', '"-1.1"', '"abc"'], '"', "", ['"1"', '"-1.1"', '"abc"']],
            [['"1"', '"-1.1"', '"abc"'], None, None, ['"1"', '"-1.1"', '"abc"']],
        ],
    )
    def test_normal_strip_str(
        self, dp_extractor, value, strip_str_header, strip_str_value, expected
    ):
        dp_extractor.strip_str_header = strip_str_header
        dp_extractor.strip_str_value = strip_str_value
        dp_list = dp_extractor.to_dp_list(value)

        for dp, value in zip(dp_list, expected):
            assert dp.data == value


class Test_DataPropertyExtractor_to_column_dp_list(object):
    TEST_DATA_MATRIX = [
        [1, 1.1, "aa", 1, 1, True, inf, nan, datetime.datetime(2017, 1, 1, 0, 0, 0)],
        [2, 2.2, "bbb", 2.2, 2.2, False, "inf", "nan", "2017-01-01T01:23:45+0900"],
        [3, 3.33, "cccc", -3, "ccc", "true", "infinity", "NAN", "2017-11-01 01:23:45+0900"],
    ]
    TEST_DATA_MATRIX_TUPLE = (
        (1, 1.1, "aa", 1, 1, True, inf, nan, datetime.datetime(2017, 1, 1, 0, 0, 0)),
        (2, 2.2, "bbb", 2.2, 2.2, False, "inf", "nan", "2017-01-01T01:23:45+0900"),
        (3, 3.33, "cccc", -3, "ccc", "true", "infinity", "NAN", "2017-11-01 01:23:45+0900"),
    )

    @pytest.mark.parametrize(
        ["max_workers", "header_list", "value"],
        [
            [1, ["i", "f", "s", "if", "mix", "bool", "inf", "nan", "time"], TEST_DATA_MATRIX],
            [4, ["i", "f", "s", "if", "mix", "bool", "inf", "nan", "time"], TEST_DATA_MATRIX],
            [None, None, TEST_DATA_MATRIX],
            [None, [], TEST_DATA_MATRIX],
            [
                None,
                ("i", "f", "s", "if", "mix", "bool", "inf", "nan", "time"),
                TEST_DATA_MATRIX_TUPLE,
            ],
        ],
    )
    def test_normal_default(self, dp_extractor, max_workers, header_list, value):
        dp_extractor.max_workers = max_workers
        dp_extractor.header_list = header_list
        col_dp_list = dp_extractor.to_column_dp_list(dp_extractor.to_dp_matrix(value))

        assert len(col_dp_list) == 9

        col_idx = 0

        dp = col_dp_list[col_idx]
        assert dp.column_index == col_idx
        assert dp.typecode == Typecode.INTEGER
        assert dp.align.align_code == Align.RIGHT.align_code
        assert dp.align.align_string == Align.RIGHT.align_string
        assert dp.ascii_char_width == 1
        assert dp.decimal_places == 0
        assert dp.format_str == "{:d}"
        assert text_type(dp) == (
            "column=0, typename=INTEGER, align=right, "
            "ascii_char_width=1, bit_len=2, integer_digits=1, decimal_places=0"
        )

        col_idx += 1
        dp = col_dp_list[col_idx]
        assert dp.column_index == col_idx
        assert dp.typecode == Typecode.REAL_NUMBER
        assert dp.align.align_code == Align.RIGHT.align_code
        assert dp.align.align_string == Align.RIGHT.align_string
        assert dp.ascii_char_width == 4
        assert dp.decimal_places == 2
        assert dp.format_str == "{:.2f}"

        col_idx += 1
        dp = col_dp_list[col_idx]
        assert dp.column_index == col_idx
        assert dp.typecode == Typecode.STRING
        assert dp.align.align_code == Align.LEFT.align_code
        assert dp.align.align_string == Align.LEFT.align_string
        assert dp.ascii_char_width == 4
        assert dp.decimal_places is None
        assert dp.format_str == "{:s}"

        col_idx += 1
        dp = col_dp_list[col_idx]
        assert dp.column_index == col_idx
        assert dp.typecode == Typecode.REAL_NUMBER
        assert dp.align.align_code == Align.RIGHT.align_code
        assert dp.align.align_string == Align.RIGHT.align_string
        assert dp.ascii_char_width == 4
        assert dp.decimal_places == 1
        assert dp.format_str == "{:.1f}"

        col_idx += 1
        dp = col_dp_list[col_idx]
        assert dp.column_index == col_idx
        assert dp.typecode == Typecode.STRING
        assert dp.align.align_code == Align.LEFT.align_code
        assert dp.align.align_string == Align.LEFT.align_string
        assert dp.ascii_char_width == 3
        assert dp.decimal_places == 1
        assert dp.format_str == "{:s}"

        col_idx += 1
        dp = col_dp_list[col_idx]
        assert dp.column_index == col_idx
        assert dp.typecode == Typecode.BOOL
        assert dp.align.align_code == Align.LEFT.align_code
        assert dp.align.align_string == Align.LEFT.align_string
        assert dp.ascii_char_width == 5
        assert dp.decimal_places is None
        assert dp.format_str == "{}"

        col_idx += 1
        dp = col_dp_list[col_idx]
        assert dp.column_index == col_idx
        assert dp.typecode == Typecode.INFINITY
        assert dp.align.align_code == Align.LEFT.align_code
        assert dp.align.align_string == Align.LEFT.align_string
        assert dp.ascii_char_width == 8
        assert dp.decimal_places is None
        assert dp.format_str == "{:f}"

        col_idx += 1
        dp = col_dp_list[col_idx]
        assert dp.column_index == col_idx
        assert dp.typecode == Typecode.NAN
        assert dp.align.align_code == Align.LEFT.align_code
        assert dp.align.align_string == Align.LEFT.align_string
        assert dp.ascii_char_width == 3
        assert dp.decimal_places is None
        assert dp.format_str == "{:f}"

        col_idx += 1
        dp = col_dp_list[col_idx]
        assert dp.column_index == col_idx
        assert dp.typecode == Typecode.STRING
        assert dp.align.align_code == Align.LEFT.align_code
        assert dp.align.align_string == Align.LEFT.align_string
        assert dp.ascii_char_width == 24
        assert dp.decimal_places is None
        assert dp.format_str == "{:s}"

    @pytest.mark.parametrize(
        ["header_list", "value"],
        [
            [["i", "f", "s", "if", "mix", "bool", "inf", "nan", "time"], TEST_DATA_MATRIX],
            [None, TEST_DATA_MATRIX],
            [[], TEST_DATA_MATRIX],
        ],
    )
    def test_normal_not_strict(self, dp_extractor, header_list, value):
        dp_extractor.header_list = header_list
        col_dp_list = dp_extractor.to_column_dp_list(dp_extractor.to_dp_matrix(value))

        assert len(col_dp_list) == 9

        dp = col_dp_list[0]
        assert dp.typecode == Typecode.INTEGER
        assert dp.align.align_code == Align.RIGHT.align_code
        assert dp.align.align_string == Align.RIGHT.align_string
        assert dp.ascii_char_width == 1
        assert dp.decimal_places == 0
        assert dp.format_str == "{:d}"

        dp = col_dp_list[1]
        assert dp.typecode == Typecode.REAL_NUMBER
        assert dp.align.align_code == Align.RIGHT.align_code
        assert dp.align.align_string == Align.RIGHT.align_string
        assert dp.ascii_char_width == 4
        assert dp.decimal_places == 2
        assert dp.format_str == "{:.2f}"

    def test_normal_col_type_hint_list(self, dp_extractor):
        dp_extractor.header_list = ["none", "to_float", "to_str", "to_datetime"]
        dp_extractor.column_type_hint_list = [None, RealNumber, String, DateTime]
        col_dp_list = dp_extractor.to_column_dp_list(
            dp_extractor.to_dp_matrix(
                [[1, "1.1", 1, "2017-01-02 03:04:05"], [2, "2.2", 0.1, "2017-01-02 03:04:05"]]
            )
        )

        assert len(col_dp_list) == 4

        col_dp = col_dp_list[0]
        assert col_dp.typecode == Typecode.INTEGER

        col_dp = col_dp_list[1]
        assert col_dp.typecode == Typecode.REAL_NUMBER

        col_dp = col_dp_list[2]
        assert col_dp.typecode == Typecode.STRING

        col_dp = col_dp_list[3]
        assert col_dp.typecode == Typecode.DATETIME

    def test_normal_nan_inf(self, dp_extractor):
        dp_extractor.header_list = ["n", "i"]
        col_dp_list = dp_extractor.to_column_dp_list(
            dp_extractor.to_dp_matrix([[nan, inf], ["nan", "inf"]])
        )

        assert len(col_dp_list) == 2

        dp = col_dp_list[0]
        assert dp.typecode == Typecode.NAN
        assert dp.align.align_code == Align.LEFT.align_code
        assert dp.align.align_string == Align.LEFT.align_string
        assert dp.ascii_char_width == 3
        assert dp.decimal_places is None

        dp = col_dp_list[1]
        assert dp.typecode == Typecode.INFINITY
        assert dp.align.align_code == Align.LEFT.align_code
        assert dp.align.align_string == Align.LEFT.align_string
        assert dp.ascii_char_width == 8
        assert dp.decimal_places is None

    @pytest.mark.parametrize(["ambiguous_width"], [[2], [1]])
    def test_normal_east_asian_ambiguous_width(self, dp_extractor, ambiguous_width):
        dp_extractor.header_list = ["ascii", "eaa"]
        dp_extractor.east_asian_ambiguous_width = ambiguous_width
        col_dp_list = dp_extractor.to_column_dp_list(
            dp_extractor.to_dp_matrix([["abcdefg", "Øαββ"], ["abcdefghij", "ØØ"]])
        )

        assert len(col_dp_list) == 2

        dp = col_dp_list[0]
        assert dp.typecode == Typecode.STRING
        assert dp.align.align_code == Align.LEFT.align_code
        assert dp.align.align_string == Align.LEFT.align_string
        assert dp.ascii_char_width == 10
        assert dp.decimal_places is None

        dp = col_dp_list[1]
        assert dp.typecode == Typecode.STRING
        assert dp.align.align_code == Align.LEFT.align_code
        assert dp.align.align_string == Align.LEFT.align_string
        assert dp.ascii_char_width == 4 * ambiguous_width
        assert dp.decimal_places is None

    def test_normal_empty_value(self, dp_extractor):
        dp_extractor.header_list = ["a", "22", "cccc"]
        col_dp_list = dp_extractor.to_column_dp_list(dp_extractor.to_dp_matrix(None))

        dp = col_dp_list[0]
        assert dp.typecode == Typecode.NONE
        assert dp.align.align_code == Align.LEFT.align_code
        assert dp.align.align_string == Align.LEFT.align_string
        assert dp.ascii_char_width == 1
        assert dp.decimal_places is None
        assert dp.format_str == "{}"

        dp = col_dp_list[1]
        assert dp.typecode == Typecode.NONE
        assert dp.align.align_code == Align.LEFT.align_code
        assert dp.align.align_string == Align.LEFT.align_string
        assert dp.ascii_char_width == 2
        assert dp.decimal_places is None
        assert dp.format_str == "{}"

        dp = col_dp_list[2]
        assert dp.typecode == Typecode.NONE
        assert dp.align.align_code == Align.LEFT.align_code
        assert dp.align.align_string == Align.LEFT.align_string
        assert dp.ascii_char_width == 4
        assert dp.decimal_places is None
        assert dp.format_str == "{}"


class Test_DataPropertyExtractor_matrix_formatting(object):
    TEST_DATA_MATRIX_NORMAL_COL3 = [["a", 0, "aa"], ["b", 1, "bb"], ["c", 2, "ccc"]]
    TEST_DATA_MATRIX_NOUNIFORM_COL1 = [["a", 0], ["b", 1, "bb"], ["c", 2, "ccc", 0.1], ["d"]]

    @pytest.mark.parametrize(
        ["header_list", "value", "matrix_formatting", "expected"],
        [
            [None, TEST_DATA_MATRIX_NOUNIFORM_COL1, MatrixFormatting.TRIM, 1],
            [["a", "b"], TEST_DATA_MATRIX_NORMAL_COL3, MatrixFormatting.TRIM, 2],
            [None, TEST_DATA_MATRIX_NOUNIFORM_COL1, MatrixFormatting.FILL_NONE, 4],
            [["a", "b", "c"], TEST_DATA_MATRIX_NORMAL_COL3, MatrixFormatting.FILL_NONE, 3],
            [["a", "b", "c"], TEST_DATA_MATRIX_NOUNIFORM_COL1, MatrixFormatting.HEADER_ALIGNED, 3],
            [
                ["a", "b", "c", "d", "e"],
                TEST_DATA_MATRIX_NOUNIFORM_COL1,
                MatrixFormatting.HEADER_ALIGNED,
                5,
            ],
        ],
    )
    def test_normal_matrix_formatting(
        self, dp_extractor, header_list, value, matrix_formatting, expected
    ):
        dp_extractor.header_list = header_list
        dp_extractor.matrix_formatting = matrix_formatting
        col_dp_list = dp_extractor.to_column_dp_list(dp_extractor.to_dp_matrix(value))

        assert len(col_dp_list) == expected

    @pytest.mark.parametrize(
        ["header_list", "value", "matrix_formatting", "expected"],
        [
            [
                ["i", "f", "s", "if", "mix"],
                TEST_DATA_MATRIX_NOUNIFORM_COL1,
                MatrixFormatting.EXCEPTION,
                ValueError,
            ]
        ],
    )
    def test_exception_matrix_formatting(
        self, dp_extractor, header_list, value, matrix_formatting, expected
    ):
        dp_extractor.header_list = header_list
        dp_extractor.matrix_formatting = matrix_formatting

        with pytest.raises(expected):
            dp_extractor.to_column_dp_list(dp_extractor.to_dp_matrix(value))
