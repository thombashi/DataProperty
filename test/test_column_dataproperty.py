# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

from __future__ import unicode_literals

import datetime
from decimal import Decimal
from ipaddress import ip_address

import pytest
import six
from six import text_type
from termcolor import colored
from typepy import (
    Bool,
    DateTime,
    Dictionary,
    Infinity,
    Integer,
    IpAddress,
    List,
    Nan,
    NoneType,
    NullString,
    RealNumber,
    String,
    Typecode,
)

from dataproperty import Align, ColumnDataProperty, DataProperty, Format


nan = float("nan")
inf = float("inf")


class Test_ColumnDataPeroperty(object):
    DATATIME_DATA = datetime.datetime(2017, 1, 1, 1, 2, 3)

    @pytest.mark.parametrize(
        ["values", "expected_typecode", "expected_class"],
        [
            # single type values
            [[None, None], Typecode.NONE, NoneType],
            [[0, six.MAXSIZE, text_type(six.MAXSIZE), -six.MAXSIZE], Typecode.INTEGER, Integer],
            [[0, 1.1, "0.01", -six.MAXSIZE], Typecode.REAL_NUMBER, RealNumber],
            [["-0.538882625371217", "0.268624155343302", ""], Typecode.REAL_NUMBER, RealNumber],
            [[ip_address("127.0.0.1"), ip_address("::1")], Typecode.IP_ADDRESS, IpAddress],
            [[0, 1.1, -six.MAXSIZE, "test"], Typecode.STRING, String],
            [["", ""], Typecode.NULL_STRING, NullString],
            [[True, True, False], Typecode.BOOL, Bool],
            [[True, "True", False], Typecode.STRING, String],
            [[DATATIME_DATA, DATATIME_DATA], Typecode.DATETIME, DateTime],
            [["2017-01-01 00:00:00", "2017-01-02 03:04:05+09:00"], Typecode.STRING, String],
            [[inf, "inf", "infinity", "INF"], Typecode.INFINITY, Infinity],
            [[nan, "nan", "NAN"], Typecode.NAN, Nan],
            [[{"a": 1}, {"b": 2}], Typecode.DICTIONARY, Dictionary],
            [[[1, 2], ["a", "b"]], Typecode.LIST, List],
            # not mixed types with None value
            [[None, six.MAXSIZE, text_type(-six.MAXSIZE)], Typecode.INTEGER, Integer],
            [[1, None, ""], Typecode.INTEGER, Integer],
            [[1.1, None], Typecode.REAL_NUMBER, RealNumber],
            [[1.1, None, ""], Typecode.REAL_NUMBER, RealNumber],
            [[0, 1.1, Decimal("0.1"), None, ""], Typecode.REAL_NUMBER, RealNumber],
            [
                [ip_address("192.168.0.1"), None, ip_address("::1"), None],
                Typecode.IP_ADDRESS,
                IpAddress,
            ],
            [[None, "test"], Typecode.STRING, String],
            [[None, True, False], Typecode.BOOL, Bool],
            [[None, True, "False"], Typecode.STRING, String],
            [[None, DATATIME_DATA, None], Typecode.DATETIME, DateTime],
            [[None, inf], Typecode.INFINITY, Infinity],
            [[None, nan], Typecode.NAN, Nan],
            # mixed types
            [[True, 1], Typecode.STRING, String],
            [[DATATIME_DATA, "test"], Typecode.STRING, String],
            [[inf, 0.1], Typecode.REAL_NUMBER, RealNumber],
            [[inf, "test"], Typecode.STRING, String],
            [[nan, 0.1], Typecode.REAL_NUMBER, RealNumber],
            [[nan, "test"], Typecode.STRING, String],
            [[six.MAXSIZE, inf, nan], Typecode.REAL_NUMBER, RealNumber],
            [[DATATIME_DATA, text_type(DATATIME_DATA), DATATIME_DATA], Typecode.STRING, String],
            [[1, 1.1, DATATIME_DATA, "test", None, True, inf, Nan], Typecode.STRING, String],
        ],
    )
    def test_normal_typecode_type_class(self, values, expected_typecode, expected_class):
        col_dp = ColumnDataProperty()
        col_dp.update_header(DataProperty("dummy"))

        for value in values:
            col_dp.update_body(DataProperty(value))

        assert col_dp.typecode == expected_typecode
        assert col_dp.type_class == expected_class

    def test_normal_number_0(self):
        col_dp = ColumnDataProperty()
        col_dp.update_header(DataProperty("abc"))

        for value in [0, -1.234, 55.55]:
            col_dp.update_body(DataProperty(value))

        assert col_dp.align == Align.RIGHT
        assert col_dp.decimal_places == 3
        assert col_dp.typecode == Typecode.REAL_NUMBER
        assert col_dp.ascii_char_width == 6

        assert col_dp.minmax_integer_digits.min_value == 1
        assert col_dp.minmax_integer_digits.max_value == 2

        assert col_dp.minmax_decimal_places.min_value == 0
        assert col_dp.minmax_decimal_places.max_value == 3

        assert col_dp.minmax_additional_format_len.min_value == 0
        assert col_dp.minmax_additional_format_len.max_value == 1

        assert text_type(col_dp) == (
            "type=REAL_NUMBER, align=right, ascii_width=6, "
            "int_digits=(min=1, max=2), decimal_places=(min=0, max=3), "
            "extra_len=(min=0, max=1)"
        )

    def test_normal_number_1(self):
        col_dp = ColumnDataProperty()
        col_dp.update_header(DataProperty("abc"))

        for value in [0, inf, nan]:
            col_dp.update_body(DataProperty(value))

        assert col_dp.align == Align.RIGHT
        assert col_dp.decimal_places == 0
        assert col_dp.typecode == Typecode.REAL_NUMBER
        assert col_dp.ascii_char_width == 8

        assert col_dp.minmax_integer_digits.min_value == 1
        assert col_dp.minmax_integer_digits.max_value == 1

        assert col_dp.minmax_decimal_places.min_value == 0
        assert col_dp.minmax_decimal_places.max_value == 0

        assert col_dp.minmax_additional_format_len.min_value == 0
        assert col_dp.minmax_additional_format_len.max_value == 0

        assert text_type(col_dp) == (
            "type=REAL_NUMBER, align=right, ascii_width=8, " "int_digits=1, decimal_places=0"
        )

    def test_normal_number_2(self):
        col_dp = ColumnDataProperty()
        col_dp.update_header(DataProperty("abc"))

        for value in [1, 2.2, -3]:
            col_dp.update_body(DataProperty(value))

        assert col_dp.align == Align.RIGHT
        assert col_dp.decimal_places == 1
        assert col_dp.typecode == Typecode.REAL_NUMBER
        assert col_dp.ascii_char_width == 4

        assert col_dp.minmax_integer_digits.min_value == 1
        assert col_dp.minmax_integer_digits.max_value == 1

        assert col_dp.minmax_decimal_places.min_value == 0
        assert col_dp.minmax_decimal_places.max_value == 1

        assert col_dp.minmax_additional_format_len.min_value == 0
        assert col_dp.minmax_additional_format_len.max_value == 1

        assert text_type(col_dp) == (
            "type=REAL_NUMBER, align=right, ascii_width=4, "
            "int_digits=1, decimal_places=(min=0, max=1), "
            "extra_len=(min=0, max=1)"
        )

    def test_normal_number_3(self):
        col_dp = ColumnDataProperty()
        col_dp.update_header(DataProperty("abc"))

        for value in [0.01, 2.2, None]:
            col_dp.update_body(DataProperty(value))

        assert col_dp.align == Align.RIGHT
        assert col_dp.decimal_places == 2
        assert col_dp.typecode == Typecode.REAL_NUMBER
        assert col_dp.ascii_char_width == 4

        assert col_dp.minmax_integer_digits.min_value == 1
        assert col_dp.minmax_integer_digits.max_value == 1

        assert col_dp.minmax_decimal_places.min_value == 1
        assert col_dp.minmax_decimal_places.max_value == 2

        assert col_dp.minmax_additional_format_len.min_value == 0
        assert col_dp.minmax_additional_format_len.max_value == 0

        assert text_type(col_dp) == (
            "type=REAL_NUMBER, align=right, ascii_width=4, "
            "int_digits=1, decimal_places=(min=1, max=2)"
        )

    def test_normal_number_4(self):
        col_dp = ColumnDataProperty()
        col_dp.update_header(DataProperty("abc"))

        for value in [0.01, 1.0, 1.2]:
            col_dp.update_body(DataProperty(value))

        assert col_dp.align == Align.RIGHT
        assert col_dp.decimal_places == 2
        assert col_dp.typecode == Typecode.REAL_NUMBER
        assert col_dp.ascii_char_width == 4

        assert col_dp.minmax_integer_digits.min_value == 1
        assert col_dp.minmax_integer_digits.max_value == 1

        assert col_dp.minmax_decimal_places.min_value == 0
        assert col_dp.minmax_decimal_places.max_value == 2
        assert col_dp.minmax_additional_format_len.min_value == 0
        assert col_dp.minmax_additional_format_len.max_value == 0

        assert text_type(col_dp) == (
            "type=REAL_NUMBER, align=right, ascii_width=4, "
            "int_digits=1, decimal_places=(min=0, max=2)"
        )

    def test_normal_number_5(self):
        col_dp = ColumnDataProperty()
        col_dp.update_header(DataProperty("abc"))

        for value in [1.1, 2.2, 3.33]:
            col_dp.update_body(DataProperty(value))

        assert col_dp.align == Align.RIGHT
        assert col_dp.decimal_places == 2
        assert col_dp.typecode == Typecode.REAL_NUMBER
        assert col_dp.ascii_char_width == 4

        assert col_dp.minmax_integer_digits.min_value == 1
        assert col_dp.minmax_integer_digits.max_value == 1

        assert col_dp.minmax_decimal_places.min_value == 1
        assert col_dp.minmax_decimal_places.max_value == 2
        assert col_dp.minmax_additional_format_len.min_value == 0
        assert col_dp.minmax_additional_format_len.max_value == 0

        assert text_type(col_dp) == (
            "type=REAL_NUMBER, align=right, ascii_width=4, "
            "int_digits=1, decimal_places=(min=1, max=2)"
        )

    def test_normal_inf(self):
        col_dp = ColumnDataProperty()
        col_dp.update_header(DataProperty("inf"))

        for value in [inf, None, inf, "inf"]:
            col_dp.update_body(DataProperty(value))

        assert col_dp.align == Align.LEFT
        assert col_dp.decimal_places is None
        assert col_dp.typecode == Typecode.INFINITY
        assert col_dp.ascii_char_width == 8

        assert col_dp.minmax_integer_digits.min_value is None
        assert col_dp.minmax_integer_digits.max_value is None

        assert col_dp.minmax_decimal_places.min_value is None
        assert col_dp.minmax_decimal_places.max_value is None

        assert col_dp.minmax_additional_format_len.min_value == 0
        assert col_dp.minmax_additional_format_len.max_value == 0

        assert text_type(col_dp) == ("type=INFINITY, align=left, ascii_width=8")

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

        assert text_type(col_dp) == (
            "type=STRING, align=left, ascii_width=7, "
            "int_digits=(min=1, max=2), decimal_places=(min=0, max=3), "
            "extra_len=(min=0, max=1)"
        )

    def test_normal_number_ansi_escape(self):
        col_dp = ColumnDataProperty()
        col_dp.update_header(DataProperty("abc"))

        for value in [colored(1, "red"), colored(2.2, "green"), colored(-3, "blue")]:
            col_dp.update_body(DataProperty(value))

        assert col_dp.align == Align.RIGHT
        assert col_dp.decimal_places == 1
        assert col_dp.typecode == Typecode.REAL_NUMBER
        assert col_dp.ascii_char_width == 4

        assert col_dp.minmax_integer_digits.min_value == 1
        assert col_dp.minmax_integer_digits.max_value == 1

        assert col_dp.minmax_decimal_places.min_value == 0
        assert col_dp.minmax_decimal_places.max_value == 1

        assert col_dp.minmax_additional_format_len.min_value == 0
        assert col_dp.minmax_additional_format_len.max_value == 1

        assert text_type(col_dp) == (
            "type=REAL_NUMBER, align=right, ascii_width=4, "
            "int_digits=1, decimal_places=(min=0, max=1), "
            "extra_len=(min=0, max=1)"
        )

    def test_normal_mix_ansi_escape(self):
        col_dp = ColumnDataProperty()
        col_dp.update_header(DataProperty("abc"))

        for value in [
            colored(0, "red"),
            colored(-1.234, "yellow"),
            colored(55.55, "green"),
            colored("abcdefg", "blue"),
        ]:
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

        assert text_type(col_dp) == (
            "type=STRING, align=left, ascii_width=7, "
            "int_digits=(min=1, max=2), decimal_places=(min=0, max=3), "
            "extra_len=(min=0, max=1)"
        )

    @pytest.mark.parametrize(["values", "expected"], [[[0, 1, 0, 1], 1], [[-128, 0, 127, None], 8]])
    def test_normal_bit_length(self, values, expected):
        col_dp = ColumnDataProperty()
        col_dp.update_header(DataProperty("dummy"))

        for value in values:
            col_dp.update_body(DataProperty(value))

        assert col_dp.typecode == Typecode.INTEGER
        assert col_dp.bit_length == expected

    @pytest.mark.parametrize(["values", "expected"], [[[0.1, 1], None], [["aaa", "0.0.0.0"], None]])
    def test_abnormal_bit_length(self, values, expected):
        col_dp = ColumnDataProperty()
        col_dp.update_header(DataProperty("dummy"))

        for value in values:
            col_dp.update_body(DataProperty(value))

        assert col_dp.bit_length == expected

    def test_normal_multibyte_char(self):
        col_dp = ColumnDataProperty()
        col_dp.update_header(DataProperty("abc"))

        for value in ["いろは", "abcde"]:
            col_dp.update_body(DataProperty(value))

        assert col_dp.align == Align.LEFT
        assert col_dp.decimal_places is None
        assert col_dp.typecode == Typecode.STRING
        assert col_dp.ascii_char_width == 6

        assert col_dp.minmax_integer_digits.min_value is None
        assert col_dp.minmax_integer_digits.max_value is None

        assert col_dp.minmax_decimal_places.min_value is None
        assert col_dp.minmax_decimal_places.max_value is None

        assert col_dp.minmax_additional_format_len.min_value == 0
        assert col_dp.minmax_additional_format_len.max_value == 0

        assert text_type(col_dp) == ("type=STRING, align=left, ascii_width=6")

    @pytest.mark.parametrize(["ambiguous_width", "ascii_char_width"], [[2, 6], [1, 3]])
    def test_normal_east_asian_ambiguous_width(self, ambiguous_width, ascii_char_width):
        col_dp = ColumnDataProperty(east_asian_ambiguous_width=ambiguous_width)
        col_dp.update_header(DataProperty("abc"))

        for value in ["ØØØ", "α", "ββ"]:
            col_dp.update_body(DataProperty(value, east_asian_ambiguous_width=ambiguous_width))

        assert col_dp.align == Align.LEFT
        assert col_dp.decimal_places is None
        assert col_dp.typecode == Typecode.STRING
        assert col_dp.ascii_char_width == ascii_char_width

        assert col_dp.minmax_integer_digits.min_value is None
        assert col_dp.minmax_integer_digits.max_value is None

        assert col_dp.minmax_decimal_places.min_value is None
        assert col_dp.minmax_decimal_places.max_value is None

        assert col_dp.minmax_additional_format_len.min_value == 0
        assert col_dp.minmax_additional_format_len.max_value == 0

    def test_min_width(self):
        min_width = 100

        col_dp = ColumnDataProperty(min_width=min_width)
        col_dp.update_header(DataProperty("abc"))

        for value in [0, -1.234, 55.55]:
            col_dp.update_body(DataProperty(value))

        assert col_dp.align == Align.RIGHT
        assert col_dp.decimal_places == 3
        assert col_dp.typecode == Typecode.REAL_NUMBER
        assert col_dp.ascii_char_width == min_width

        assert col_dp.minmax_integer_digits.min_value == 1
        assert col_dp.minmax_integer_digits.max_value == 2

        assert col_dp.minmax_decimal_places.min_value == 0
        assert col_dp.minmax_decimal_places.max_value == 3

        assert col_dp.minmax_additional_format_len.min_value == 0
        assert col_dp.minmax_additional_format_len.max_value == 1

        assert text_type(col_dp) == (
            "type=REAL_NUMBER, align=right, ascii_width=100, "
            "int_digits=(min=1, max=2), decimal_places=(min=0, max=3), "
            "extra_len=(min=0, max=1)"
        )

    def test_extend_width(self):
        col_dp = ColumnDataProperty()
        col_dp.update_header(DataProperty("abc"))

        assert col_dp.ascii_char_width == 3

        col_dp.extend_width(2)

        assert col_dp.ascii_char_width == 5

    def test_null(self):
        col_dp = ColumnDataProperty()
        assert col_dp.align == Align.LEFT
        assert col_dp.decimal_places is None
        assert col_dp.typecode == Typecode.NONE
        assert col_dp.ascii_char_width == 0


class Test_ColumnDataPeroperty_dp_to_str(object):
    def test_normal_0(self):
        col_dp = ColumnDataProperty()
        values = [0.1, 3.4375, 65.5397978633, 189.74439359, 10064.0097539, "abcd"]
        expected_list = ["0.100", "3.437", "65.540", "189.744", "10064.010", "abcd"]

        col_dp.update_header(DataProperty("abc"))
        for value in values:
            col_dp.update_body(DataProperty(value))

        for value, expected in zip(values, expected_list):
            assert col_dp.dp_to_str(DataProperty(value)) == expected

    def test_normal_1(self):
        col_dp = ColumnDataProperty()
        values = [0, 0.1]
        expected_list = ["0", "0.1"]

        col_dp.update_header(DataProperty("abc"))
        for value in ["abcd", "efg"]:
            col_dp.update_body(DataProperty(value))

        for value, expected in zip(values, expected_list):
            assert col_dp.dp_to_str(DataProperty(value)) == expected

    def test_normal_2(self):
        col_dp = ColumnDataProperty()
        values = [1.1, 2.2, 3.33]
        expected_list = ["1.10", "2.20", "3.33"]

        col_dp.update_header(DataProperty("abc"))
        for value in values:
            col_dp.update_body(DataProperty(value))

        for value, expected in zip(values, expected_list):
            assert col_dp.dp_to_str(DataProperty(value)) == expected

    @pytest.mark.parametrize(
        ["values", "expected_list"],
        [
            [[1234, 223, 1234567], ["1,234", "223", "1,234,567"]],
            [[1234.1, 223.33, 1234567.33], ["1,234.1", "223.3", "1,234,567.3"]],
        ],
    )
    def test_normal_format(self, values, expected_list):
        col_dp = ColumnDataProperty(format_flags=Format.THOUSAND_SEPARATOR)

        col_dp.update_header(DataProperty("format test"))
        for value in values:
            col_dp.update_body(DataProperty(value))

        for value, expected in zip(values, expected_list):
            assert col_dp.dp_to_str(DataProperty(value)) == expected
