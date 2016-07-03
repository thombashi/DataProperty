# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <gogogo.vm@gmail.com>
"""

import datetime

import pytest
import six


from dataproperty import is_nan
from dataproperty import Align
from dataproperty import ColumnDataProperty
from dataproperty import DataProperty
from dataproperty import Typecode


nan = float("nan")
inf = float("inf")


class Test_ColumnDataPeroperty:
    DATATIME_DATA = datetime.datetime(2017, 1, 1)

    @pytest.mark.parametrize(["value_list", "expected"], [
        # single type values
        [[None, None], Typecode.NONE],
        [
            [0, six.MAXSIZE, str(six.MAXSIZE), -six.MAXSIZE],
            Typecode.INT,
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
            Typecode.DATETIME,
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
        [[None, six.MAXSIZE, str(-six.MAXSIZE)], Typecode.INT],
        [[1.0, None], Typecode.FLOAT],
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
        col_prop = ColumnDataProperty()
        col_prop.update_header(DataProperty("dummy"))

        for value in value_list:
            col_prop.update_body(DataProperty(value))

        assert col_prop.typecode == expected

    def test_normal_number_0(self):
        col_prop = ColumnDataProperty()
        col_prop.update_header(DataProperty("abc"))

        for value in [0, -1.234, 55.55]:
            col_prop.update_body(DataProperty(value))

        assert col_prop.align == Align.RIGHT
        assert col_prop.decimal_places == 2
        assert col_prop.typecode == Typecode.FLOAT
        assert col_prop.padding_len == 6

        assert col_prop.minmax_integer_digits.min_value == 1
        assert col_prop.minmax_integer_digits.max_value == 2

        assert col_prop.minmax_decimal_places.min_value == 0
        assert col_prop.minmax_decimal_places.max_value == 3

        assert col_prop.minmax_additional_format_len.min_value == 0
        assert col_prop.minmax_additional_format_len.max_value == 1

        assert str(col_prop) == (
            "typename=FLOAT, align=right, padding_len=6, "
            "integer_digits=(min=1, max=2), decimal_places=(min=0, max=3), "
            "additional_format_len=(min=0, max=1)")

    def test_normal_number_1(self):
        col_prop = ColumnDataProperty()
        col_prop.update_header(DataProperty("abc"))

        for value in [0, inf, nan]:
            col_prop.update_body(DataProperty(value))

        assert col_prop.align == Align.RIGHT
        assert col_prop.decimal_places == 0
        assert col_prop.typecode == Typecode.FLOAT
        assert col_prop.padding_len == 3

        assert col_prop.minmax_integer_digits.min_value == 1
        assert col_prop.minmax_integer_digits.max_value == 1

        assert col_prop.minmax_decimal_places.min_value == 0
        assert col_prop.minmax_decimal_places.max_value == 0

        assert col_prop.minmax_additional_format_len.min_value == 0
        assert col_prop.minmax_additional_format_len.max_value == 0

        assert str(col_prop) == (
            "typename=FLOAT, align=right, padding_len=3, "
            "integer_digits=(min=1, max=1), decimal_places=(min=0, max=0), "
            "additional_format_len=(min=0, max=0)")

    def test_normal_number_2(self):
        col_prop = ColumnDataProperty()
        col_prop.update_header(DataProperty("abc"))

        for value in [1, 2.2, -3]:
            col_prop.update_body(DataProperty(value))

        assert col_prop.align == Align.RIGHT
        assert col_prop.decimal_places == 1
        assert col_prop.typecode == Typecode.FLOAT
        assert col_prop.padding_len == 4

        assert col_prop.minmax_integer_digits.min_value == 1
        assert col_prop.minmax_integer_digits.max_value == 1

        assert col_prop.minmax_decimal_places.min_value == 0
        assert col_prop.minmax_decimal_places.max_value == 1

        assert col_prop.minmax_additional_format_len.min_value == 0
        assert col_prop.minmax_additional_format_len.max_value == 1

        assert str(col_prop) == (
            "typename=FLOAT, align=right, padding_len=4, "
            "integer_digits=(min=1, max=1), decimal_places=(min=0, max=1), "
            "additional_format_len=(min=0, max=1)")

    def test_normal_number_3(self):
        col_prop = ColumnDataProperty()
        col_prop.update_header(DataProperty("abc"))

        for value in [1.0, 2.2, None]:
            col_prop.update_body(DataProperty(value))

        assert col_prop.align == Align.RIGHT
        assert col_prop.decimal_places == 1
        assert col_prop.typecode == Typecode.FLOAT
        assert col_prop.padding_len == 4

        assert col_prop.minmax_integer_digits.min_value == 1
        assert col_prop.minmax_integer_digits.max_value == 1

        assert col_prop.minmax_decimal_places.min_value == 1
        assert col_prop.minmax_decimal_places.max_value == 1

        assert col_prop.minmax_additional_format_len.min_value == 0
        assert col_prop.minmax_additional_format_len.max_value == 0

        assert str(col_prop) == (
            "typename=FLOAT, align=right, padding_len=4, "
            "integer_digits=(min=1, max=1), decimal_places=(min=1, max=1), "
            "additional_format_len=(min=0, max=0)")

    def test_normal_mix_0(self):
        col_prop = ColumnDataProperty()
        col_prop.update_header(DataProperty("abc"))

        for value in [0, -1.234, 55.55, "abcdefg"]:
            col_prop.update_body(DataProperty(value))

        assert col_prop.align == Align.LEFT
        assert col_prop.decimal_places == 2
        assert col_prop.typecode == Typecode.STRING
        assert col_prop.padding_len == 7

        assert col_prop.minmax_integer_digits.min_value == 1
        assert col_prop.minmax_integer_digits.max_value == 2

        assert col_prop.minmax_decimal_places.min_value == 0
        assert col_prop.minmax_decimal_places.max_value == 3

        assert col_prop.minmax_additional_format_len.min_value == 0
        assert col_prop.minmax_additional_format_len.max_value == 1

        assert str(col_prop) == (
            "typename=STRING, align=left, padding_len=7, "
            "integer_digits=(min=1, max=2), decimal_places=(min=0, max=3), "
            "additional_format_len=(min=0, max=1)")

    def test_min_padding_len(self):
        min_padding_len = 100

        col_prop = ColumnDataProperty(min_padding_len)
        col_prop.update_header(DataProperty("abc"))

        for value in [0, -1.234, 55.55]:
            col_prop.update_body(DataProperty(value))

        assert col_prop.align == Align.RIGHT
        assert col_prop.decimal_places == 2
        assert col_prop.typecode == Typecode.FLOAT
        assert col_prop.padding_len == min_padding_len

        assert col_prop.minmax_integer_digits.min_value == 1
        assert col_prop.minmax_integer_digits.max_value == 2

        assert col_prop.minmax_decimal_places.min_value == 0
        assert col_prop.minmax_decimal_places.max_value == 3

        assert col_prop.minmax_additional_format_len.min_value == 0
        assert col_prop.minmax_additional_format_len.max_value == 1

        assert str(col_prop) == (
            "typename=FLOAT, align=right, padding_len=100, "
            "integer_digits=(min=1, max=2), decimal_places=(min=0, max=3), "
            "additional_format_len=(min=0, max=1)")

    def test_null(self):
        col_prop = ColumnDataProperty()
        assert col_prop.align == Align.LEFT
        assert is_nan(col_prop.decimal_places)
        assert col_prop.typecode == Typecode.NONE
        assert col_prop.padding_len == 0
