# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

from __future__ import unicode_literals

import datetime
from decimal import Decimal

import pytest
import six
from six import text_type
from typepy import DateTime, RealNumber, String, Typecode

from dataproperty import (
    Align,
    DataPropertyExtractor,
    Format,
    LineBreakHandling,
    MatrixFormatting,
    Preprocessor,
)

from .common import get_strict_level_map


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


def trans_func_1(v):
    if v is None:
        return ""
    if v is False:
        return "false"
    if v == 0:
        return 123
    return v


def trans_func_2(v):
    if v == 123:
        return 321
    return v


def nop(v):
    return v


class Test_DataPropertyExtractor_to_dp(object):
    @pytest.mark.parametrize(
        ["value", "type_value_map", "is_strict", "expected_value", "expected_typecode"],
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
    def test_normal_type_value_map(
        self, dp_extractor, value, type_value_map, is_strict, expected_value, expected_typecode
    ):
        dp_extractor.type_value_map = type_value_map
        dp_extractor.strict_level_map = get_strict_level_map(is_strict)
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
        dp_extractor.strict_level_map = get_strict_level_map(is_strict)
        dp = dp_extractor.to_dp(value)

        assert dp.data == expected

    @pytest.mark.parametrize(
        ["value", "type_hint", "trans_func", "expected"],
        [
            [1, String, nop, "1"],
            [0, String, nop, "0"],
            [None, String, nop, "None"],
            [0, String, trans_func_1, "123"],
            [False, String, trans_func_1, "false"],
            [None, String, trans_func_1, ""],
        ],
    )
    def test_normal_type_hint(self, dp_extractor, value, type_hint, trans_func, expected):
        dp_extractor.register_trans_func(trans_func)
        dp = dp_extractor._DataPropertyExtractor__to_dp(value, type_hint=type_hint)

        assert dp.data == expected

    @pytest.mark.parametrize(
        ["value", "type_hint", "trans_funcs", "expected"],
        [
            [0, String, [trans_func_2, trans_func_1], "321"],
            [0, String, [trans_func_1, trans_func_2], "123"],
        ],
    )
    def test_normal_trans_funcs(self, dp_extractor, value, type_hint, trans_funcs, expected):
        for trans_func in trans_funcs:
            dp_extractor.register_trans_func(trans_func)
        dp = dp_extractor._DataPropertyExtractor__to_dp(value, type_hint=type_hint)

        assert dp.data == expected


class Test_DataPropertyExtractor_to_dp_quoting_flags(object):
    ALWAYS_QUOTE_FLAG_MAP = {
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
        ["value", "quoting_flags", "expected"],
        [
            ["string", ALWAYS_QUOTE_FLAG_MAP, '"string"'],
            ['"string"', ALWAYS_QUOTE_FLAG_MAP, '"string"'],
            [' "123"', ALWAYS_QUOTE_FLAG_MAP, ' "123"'],
            ['"string" ', ALWAYS_QUOTE_FLAG_MAP, '"string" '],
            [' "12 345" ', ALWAYS_QUOTE_FLAG_MAP, ' "12 345" '],
        ],
    )
    def test_normal_always_quote(self, dp_extractor, value, quoting_flags, expected):
        dp_extractor.quoting_flags = quoting_flags
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
        ["value", "type_value_map", "datetime_formatter"],
        [
            [
                [[None, "1"], [1.1, "a"], [nan, inf], ["false", DATATIME_DATA]],
                {Typecode.NONE: "null", Typecode.INFINITY: "INFINITY", Typecode.NAN: "NAN"},
                datetime_formatter_test,
            ]
        ],
    )
    def test_normal(self, dp_extractor, value, type_value_map, datetime_formatter):
        dp_extractor.type_value_map = type_value_map
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
        dp_extractor.preprocessor = Preprocessor(strip_str=strip_str_value)
        dp_list = dp_extractor.to_dp_list(value)

        for dp, expected_value in zip(dp_list, expected):
            assert dp.data == expected_value

        dp_matrix = dp_extractor.to_dp_matrix([value])
        for dp, expected_value in zip(dp_matrix[0], expected):
            assert dp.data == expected_value

    @pytest.mark.parametrize(
        ["value", "line_break_handling", "expected"],
        [
            [["a\nb", "a\r\nb"], LineBreakHandling.NOP, ["a\nb", "a\r\nb"]],
            [["a\nb", "a\r\nb"], LineBreakHandling.REPLACE, ["a b", "a b"]],
            [["a\nb", "a\r\nb"], LineBreakHandling.ESCAPE, ["a\\nb", "a\\r\\nb"]],
        ],
    )
    def test_normal_line_break_handling(self, dp_extractor, value, line_break_handling, expected):
        dp_extractor.preprocessor = Preprocessor(line_break_handling=line_break_handling)
        dp_list = dp_extractor.to_dp_list(value)

        for dp, value in zip(dp_list, expected):
            assert dp.data == value

    @pytest.mark.parametrize(
        ["value", "line_break_handling", "line_break_repl", "expected"],
        [
            [["a\nb", "a\r\nb"], LineBreakHandling.NOP, "<br>", ["a\nb", "a\r\nb"]],
            [
                ["a\nb", "a\r\nb", "a\r\n\nb"],
                LineBreakHandling.REPLACE,
                "<br>",
                ["a<br>b", "a<br>b", "a<br><br>b"],
            ],
        ],
    )
    def test_normal_line_break_repl(
        self, dp_extractor, value, line_break_handling, line_break_repl, expected
    ):
        dp_extractor.preprocessor = Preprocessor(
            line_break_handling=line_break_handling, line_break_repl=line_break_repl
        )
        dp_list = dp_extractor.to_dp_list(value)

        for dp, value in zip(dp_list, expected):
            assert dp.data == value, value

    @pytest.mark.parametrize(
        ["value", "escape_formula_injection", "expected"],
        [
            [
                ["a+b", "=a+b", "-a+b", "+a+b", "@a+b"],
                True,
                ["a+b", "'=a+b", "'-a+b", "'+a+b", "'@a+b"],
            ],
            [
                ["a+b", "=a+b", "-a+b", "+a+b", "@a+b"],
                False,
                ["a+b", "=a+b", "-a+b", "+a+b", "@a+b"],
            ],
        ],
    )
    def test_normal_escape_formula_injection(
        self, dp_extractor, value, escape_formula_injection, expected
    ):
        dp_extractor.preprocessor = Preprocessor(
            is_escape_formula_injection=escape_formula_injection
        )
        dp_list = dp_extractor.to_dp_list(value)

        for dp, value in zip(dp_list, expected):
            assert dp.data == value, value

    @pytest.mark.parametrize(
        ["value", "expected"], [[[0, None], [0, None]]],
    )
    def test_exception_escape_formula_injection(self, dp_extractor, value, expected):
        dp_extractor.preprocessor = Preprocessor(is_escape_formula_injection=True)
        dp_list = dp_extractor.to_dp_list(value)

        for dp, value in zip(dp_list, expected):
            assert dp.data == value, value


class Test_DataPropertyExtractor_to_column_dp_list(object):
    TEST_DATA_MATRIX = [
        [1, 1.1, "aa", 1, 1, True, inf, nan, datetime.datetime(2017, 1, 1, 0, 0, 0)],
        [2, 2.2, "bbb", 2.2, 2.2, False, "inf", "nan", "2017-01-01T01:23:45+0900"],
        [3, 3.33, "cccc", -3, "ccc", True, "infinity", "NAN", "2017-11-01 01:23:45+0900"],
    ]
    TEST_DATA_MATRIX_TUPLE = (
        (1, 1.1, "aa", 1, 1, True, inf, nan, datetime.datetime(2017, 1, 1, 0, 0, 0)),
        (2, 2.2, "bbb", 2.2, 2.2, False, "inf", "nan", "2017-01-01T01:23:45+0900"),
        (3, 3.33, "cccc", -3, "ccc", True, "infinity", "NAN", "2017-11-01 01:23:45+0900"),
    )

    @pytest.mark.parametrize(
        ["max_workers", "headers", "value"],
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
    def test_normal_default(self, dp_extractor, max_workers, headers, value):
        dp_extractor.max_workers = max_workers
        dp_extractor.headers = headers
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
            "column=0, type=INTEGER, align=right, "
            "ascii_width=1, bit_len=2, int_digits=1, decimal_places=0"
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
        ["headers", "value"],
        [[["i", "f"], [[1234, 1234.5], [1234567, 34.5]]], [[], [[1234, 1234.5], [1234567, 34.5]]]],
    )
    def test_normal_format_str(self, dp_extractor, headers, value):
        dp_extractor.format_flags_list = [Format.THOUSAND_SEPARATOR, Format.THOUSAND_SEPARATOR]
        dp_extractor.max_workers = 1
        dp_extractor.headers = headers
        col_dp_list = dp_extractor.to_column_dp_list(dp_extractor.to_dp_matrix(value))

        assert len(col_dp_list) == 2

        col_idx = 0

        dp = col_dp_list[col_idx]
        assert dp.column_index == col_idx
        assert dp.typecode == Typecode.INTEGER
        assert dp.format_str == "{:,d}"
        assert dp.ascii_char_width == 9

        col_idx += 1
        dp = col_dp_list[col_idx]
        assert dp.column_index == col_idx
        assert dp.typecode == Typecode.REAL_NUMBER
        assert dp.format_str == "{:,.1f}"
        assert dp.ascii_char_width == 7

    @pytest.mark.parametrize(
        ["headers", "value"],
        [
            [["i", "f", "s", "if", "mix", "bool", "inf", "nan", "time"], TEST_DATA_MATRIX],
            [None, TEST_DATA_MATRIX],
            [[], TEST_DATA_MATRIX],
        ],
    )
    def test_normal_not_strict(self, dp_extractor, headers, value):
        dp_extractor.headers = headers
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

    def test_normal_column_type_hints(self, dp_extractor):
        dp_extractor.headers = ["none", "to_float", "to_str", "to_datetime"]
        dp_extractor.column_type_hints = [None, RealNumber, String, DateTime]
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
        dp_extractor.headers = ["n", "i"]
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
        dp_extractor.headers = ["ascii", "eaa"]
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
        dp_extractor.headers = ["a", "22", "cccc"]
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
        ["headers", "value", "matrix_formatting", "expected"],
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
        self, dp_extractor, headers, value, matrix_formatting, expected
    ):
        dp_extractor.headers = headers
        dp_extractor.matrix_formatting = matrix_formatting
        col_dp_list = dp_extractor.to_column_dp_list(dp_extractor.to_dp_matrix(value))

        assert len(col_dp_list) == expected

    @pytest.mark.parametrize(
        ["headers", "value", "matrix_formatting", "expected"],
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
        self, dp_extractor, headers, value, matrix_formatting, expected
    ):
        dp_extractor.headers = headers
        dp_extractor.matrix_formatting = matrix_formatting

        with pytest.raises(expected):
            dp_extractor.to_column_dp_list(dp_extractor.to_dp_matrix(value))


class Test_DataPropertyExtractor_update_preprocessor(object):
    def test_normal(self, dp_extractor):
        assert dp_extractor.preprocessor.strip_str is None
        assert dp_extractor.preprocessor.replace_tabs_with_spaces is True
        assert dp_extractor.preprocessor.tab_length == 2
        assert dp_extractor.preprocessor.line_break_handling is LineBreakHandling.NOP
        assert dp_extractor.preprocessor.line_break_repl == " "
        assert dp_extractor.preprocessor.is_escape_html_tag is False
        assert dp_extractor.preprocessor.is_escape_formula_injection is False

        dp_extractor.update_preprocessor(
            strip_str='"',
            replace_tabs_with_spaces=False,
            tab_length=4,
            line_break_handling=LineBreakHandling.REPLACE,
            line_break_repl="<br>",
            is_escape_html_tag=True,
            is_escape_formula_injection=True,
        )
        assert dp_extractor.preprocessor.strip_str == '"'
        assert dp_extractor.preprocessor.replace_tabs_with_spaces is False
        assert dp_extractor.preprocessor.tab_length == 4
        assert dp_extractor.preprocessor.line_break_handling is LineBreakHandling.REPLACE
        assert dp_extractor.preprocessor.line_break_repl == "<br>"
        assert dp_extractor.preprocessor.is_escape_html_tag is True
        assert dp_extractor.preprocessor.is_escape_formula_injection is True
