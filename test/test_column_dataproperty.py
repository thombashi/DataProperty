# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <gogogo.vm@gmail.com>
"""

from __future__ import unicode_literals
import datetime

import pytest
import six

from dataproperty import (
    Align,
    ColumnDataProperty,
    DataProperty,
    NanType,
    Typecode
)


nan = float("nan")
inf = float("inf")


class Test_ColumnDataPeroperty:
    DATATIME_DATA = datetime.datetime(2017, 1, 1)

    @pytest.mark.parametrize(["value_list", "expected"], [
        # single type values
        [[None, None], Typecode.NONE],
        [
            [0, six.MAXSIZE, str(six.MAXSIZE), -six.MAXSIZE],
            Typecode.INTEGER,
        ],
        [
            [0, 1.1, "0.01", -six.MAXSIZE],
            Typecode.FLOAT,
        ],
        [
            [0, 1.1, -six.MAXSIZE, "test"],
            Typecode.STRING,
        ],
        [
            [True, "True", False],
            Typecode.BOOL,
        ],
        [
            [DATATIME_DATA, str(DATATIME_DATA), DATATIME_DATA],
            Typecode.STRING,
        ],
        [
            [inf, "inf", "infinity", "INF"],
            Typecode.INFINITY,
        ],
        [
            [nan, "nan", "NAN"],
            Typecode.NAN,
        ],

        # None mixed values
        [[None, six.MAXSIZE, str(-six.MAXSIZE)], Typecode.INTEGER],
        [[1.1, None], Typecode.FLOAT],
        [[None, "test"], Typecode.STRING],
        [[None, True, "False"], Typecode.BOOL],
        [[None, DATATIME_DATA, None], Typecode.DATETIME],
        [[None, inf], Typecode.INFINITY],
        [[None, nan], Typecode.NAN],

        # mixed values
        [[True, 1], Typecode.STRING],
        [[DATATIME_DATA, "test"], Typecode.STRING],
        [[inf, 0.1], Typecode.FLOAT],
        [[inf, "test"], Typecode.STRING],
        [[nan, 0.1], Typecode.FLOAT],
        [[nan, "test"], Typecode.STRING],
        [[six.MAXSIZE, inf, nan], Typecode.FLOAT],
        [
            [1, 1.1, DATATIME_DATA, "test", None, True, inf, nan],
            Typecode.STRING,
        ],
    ])
    def test_normal_typecode(self, value_list, expected):
        col_dp = ColumnDataProperty()
        col_dp.update_header(DataProperty("dummy"))

        for value in value_list:
            col_dp.update_body(DataProperty(value))

        assert col_dp.typecode == expected

    def test_normal_number_0(self):
        col_dp = ColumnDataProperty()
        col_dp.update_header(DataProperty("abc"))

        for value in [0, -1.234, 55.55]:
            col_dp.update_body(DataProperty(value))

        assert col_dp.align == Align.RIGHT
        assert col_dp.decimal_places == 3
        assert col_dp.typecode == Typecode.FLOAT
        assert col_dp.ascii_char_width == 6

        assert col_dp.minmax_integer_digits.min_value == 1
        assert col_dp.minmax_integer_digits.max_value == 2

        assert col_dp.minmax_decimal_places.min_value == 0
        assert col_dp.minmax_decimal_places.max_value == 3

        assert col_dp.minmax_additional_format_len.min_value == 0
        assert col_dp.minmax_additional_format_len.max_value == 1

        assert str(col_dp) == (
            "typename=FLOAT, align=right, ascii_char_width=6, "
            "integer_digits=(min=1, max=2), decimal_places=(min=0, max=3), "
            "additional_format_len=(min=0, max=1)")

    def test_normal_number_1(self):
        col_dp = ColumnDataProperty()
        col_dp.update_header(DataProperty("abc"))

        for value in [0, inf, nan]:
            col_dp.update_body(DataProperty(value))

        assert col_dp.align == Align.RIGHT
        assert col_dp.decimal_places == 0
        assert col_dp.typecode == Typecode.FLOAT
        assert col_dp.ascii_char_width == 8

        assert col_dp.minmax_integer_digits.min_value == 1
        assert col_dp.minmax_integer_digits.max_value == 1

        assert col_dp.minmax_decimal_places.min_value == 0
        assert col_dp.minmax_decimal_places.max_value == 0

        assert col_dp.minmax_additional_format_len.min_value == 0
        assert col_dp.minmax_additional_format_len.max_value == 0

        assert str(col_dp) == (
            "typename=FLOAT, align=right, ascii_char_width=8, "
            "integer_digits=(min=1, max=1), decimal_places=(min=0, max=0), "
            "additional_format_len=(min=0, max=0)")

    def test_normal_number_2(self):
        col_dp = ColumnDataProperty()
        col_dp.update_header(DataProperty("abc"))

        for value in [1, 2.2, -3]:
            col_dp.update_body(DataProperty(value))

        assert col_dp.align == Align.RIGHT
        assert col_dp.decimal_places == 1
        assert col_dp.typecode == Typecode.FLOAT
        assert col_dp.ascii_char_width == 4

        assert col_dp.minmax_integer_digits.min_value == 1
        assert col_dp.minmax_integer_digits.max_value == 1

        assert col_dp.minmax_decimal_places.min_value == 0
        assert col_dp.minmax_decimal_places.max_value == 1

        assert col_dp.minmax_additional_format_len.min_value == 0
        assert col_dp.minmax_additional_format_len.max_value == 1

        assert str(col_dp) == (
            "typename=FLOAT, align=right, ascii_char_width=4, "
            "integer_digits=(min=1, max=1), decimal_places=(min=0, max=1), "
            "additional_format_len=(min=0, max=1)")

    def test_normal_number_3(self):
        col_dp = ColumnDataProperty()
        col_dp.update_header(DataProperty("abc"))

        for value in [0.01, 2.2, None]:
            col_dp.update_body(DataProperty(value))

        assert col_dp.align == Align.RIGHT
        assert col_dp.decimal_places == 2
        assert col_dp.typecode == Typecode.FLOAT
        assert col_dp.ascii_char_width == 4

        assert col_dp.minmax_integer_digits.min_value == 1
        assert col_dp.minmax_integer_digits.max_value == 1

        assert col_dp.minmax_decimal_places.min_value == 1
        assert col_dp.minmax_decimal_places.max_value == 2

        assert col_dp.minmax_additional_format_len.min_value == 0
        assert col_dp.minmax_additional_format_len.max_value == 0

        assert str(col_dp) == (
            "typename=FLOAT, align=right, ascii_char_width=4, "
            "integer_digits=(min=1, max=1), decimal_places=(min=1, max=2), "
            "additional_format_len=(min=0, max=0)")

    def test_normal_number_4(self):
        col_dp = ColumnDataProperty()
        col_dp.update_header(DataProperty("abc"))

        for value in [0.01, 1.0, 1.2]:
            col_dp.update_body(DataProperty(value))

        assert col_dp.align == Align.RIGHT
        assert col_dp.decimal_places == 2
        assert col_dp.typecode == Typecode.FLOAT
        assert col_dp.ascii_char_width == 4

        assert col_dp.minmax_integer_digits.min_value == 1
        assert col_dp.minmax_integer_digits.max_value == 1

        assert col_dp.minmax_decimal_places.min_value == 0
        assert col_dp.minmax_decimal_places.max_value == 2
        assert col_dp.minmax_additional_format_len.min_value == 0
        assert col_dp.minmax_additional_format_len.max_value == 0

        assert str(col_dp) == (
            "typename=FLOAT, align=right, ascii_char_width=4, "
            "integer_digits=(min=1, max=1), decimal_places=(min=0, max=2), "
            "additional_format_len=(min=0, max=0)")

    def test_normal_inf(self):
        col_dp = ColumnDataProperty()
        col_dp.update_header(DataProperty("inf"))

        for value in [inf, None, inf, "inf"]:
            col_dp.update_body(DataProperty(value))

        assert col_dp.align == Align.LEFT
        assert NanType(col_dp.decimal_places).is_type()
        assert col_dp.typecode == Typecode.INFINITY
        assert col_dp.ascii_char_width == 8

        assert col_dp.minmax_integer_digits.min_value is None
        assert col_dp.minmax_integer_digits.max_value is None

        assert col_dp.minmax_decimal_places.min_value is None
        assert col_dp.minmax_decimal_places.max_value is None

        assert col_dp.minmax_additional_format_len.min_value == 0
        assert col_dp.minmax_additional_format_len.max_value == 0

        assert str(col_dp) == (
            "typename=INFINITY, align=left, ascii_char_width=8, "
            "integer_digits=(min=None, max=None), decimal_places=(min=None, max=None), "
            "additional_format_len=(min=0, max=0)")

    def test_normal_mix_0(self):
        col_dp = ColumnDataProperty()
        col_dp.update_header(DataProperty("abc"))

        for value in [0, -1.234, 55.55, "abcdefg"]:
            col_dp.update_body(DataProperty(value))

        assert col_dp.align == Align.LEFT
        assert col_dp.decimal_places == 3
        assert col_dp.typecode == Typecode.STRING
        assert col_dp.ascii_char_width == 7

        assert col_dp.minmax_integer_digits.min_value == 1
        assert col_dp.minmax_integer_digits.max_value == 2

        assert col_dp.minmax_decimal_places.min_value == 0
        assert col_dp.minmax_decimal_places.max_value == 3

        assert col_dp.minmax_additional_format_len.min_value == 0
        assert col_dp.minmax_additional_format_len.max_value == 1

        assert str(col_dp) == (
            "typename=STRING, align=left, ascii_char_width=7, "
            "integer_digits=(min=1, max=2), decimal_places=(min=0, max=3), "
            "additional_format_len=(min=0, max=1)")

    def test_normal_multibyte_char(self):
        col_dp = ColumnDataProperty()
        col_dp.update_header(DataProperty("abc"))

        for value in ["いろは", "abcde"]:
            col_dp.update_body(DataProperty(value))

        assert col_dp.align == Align.LEFT
        assert NanType(col_dp.decimal_places).is_type()
        assert col_dp.typecode == Typecode.STRING
        assert col_dp.ascii_char_width == 6

        assert col_dp.minmax_integer_digits.min_value is None
        assert col_dp.minmax_integer_digits.max_value is None

        assert col_dp.minmax_decimal_places.min_value is None
        assert col_dp.minmax_decimal_places.max_value is None

        assert col_dp.minmax_additional_format_len.min_value == 0
        assert col_dp.minmax_additional_format_len.max_value == 0

        assert str(col_dp) == (
            "typename=STRING, align=left, ascii_char_width=6, "
            "integer_digits=(min=None, max=None), "
            "decimal_places=(min=None, max=None), "
            "additional_format_len=(min=0, max=0)"
        )

    @pytest.mark.parametrize(["ambiguous_width", "ascii_char_width"], [
        [2, 6],
        [1, 3],
    ])
    def test_normal_east_asian_ambiguous_width(
            self, ambiguous_width, ascii_char_width):
        col_dp = ColumnDataProperty(
            east_asian_ambiguous_width=ambiguous_width)
        col_dp.update_header(DataProperty("abc"))

        for value in ["ØØØ", "α", "ββ"]:
            col_dp.update_body(DataProperty(
                value, east_asian_ambiguous_width=ambiguous_width))

        assert col_dp.align == Align.LEFT
        assert NanType(col_dp.decimal_places).is_type()
        assert col_dp.typecode == Typecode.STRING
        assert col_dp.ascii_char_width == ascii_char_width

        assert col_dp.minmax_integer_digits.min_value is None
        assert col_dp.minmax_integer_digits.max_value is None

        assert col_dp.minmax_decimal_places.min_value is None
        assert col_dp.minmax_decimal_places.max_value is None

        assert col_dp.minmax_additional_format_len.min_value == 0
        assert col_dp.minmax_additional_format_len.max_value == 0

    def test_min_padding_len(self):
        min_padding_len = 100

        col_dp = ColumnDataProperty(min_padding_len)
        col_dp.update_header(DataProperty("abc"))

        for value in [0, -1.234, 55.55]:
            col_dp.update_body(DataProperty(value))

        assert col_dp.align == Align.RIGHT
        assert col_dp.decimal_places == 3
        assert col_dp.typecode == Typecode.FLOAT
        assert col_dp.ascii_char_width == min_padding_len

        assert col_dp.minmax_integer_digits.min_value == 1
        assert col_dp.minmax_integer_digits.max_value == 2

        assert col_dp.minmax_decimal_places.min_value == 0
        assert col_dp.minmax_decimal_places.max_value == 3

        assert col_dp.minmax_additional_format_len.min_value == 0
        assert col_dp.minmax_additional_format_len.max_value == 1

        assert str(col_dp) == (
            "typename=FLOAT, align=right, ascii_char_width=100, "
            "integer_digits=(min=1, max=2), decimal_places=(min=0, max=3), "
            "additional_format_len=(min=0, max=1)")

    def test_null(self):
        col_dp = ColumnDataProperty()
        assert col_dp.align == Align.LEFT
        assert NanType(col_dp.decimal_places).is_type()
        assert col_dp.typecode == Typecode.NONE
        assert col_dp.ascii_char_width == 0
