# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

from __future__ import print_function, unicode_literals

import datetime
import ipaddress
import sys
from decimal import Decimal

import pytest
import six
from six import text_type
from termcolor import colored
from typepy import Bool, DateTime, Integer, Nan, RealNumber, StrictLevel, String, Typecode

from dataproperty import (
    MIN_STRICT_LEVEL_MAP,
    Align,
    DataProperty,
    DefaultValue,
    Format,
    LineBreakHandling,
    Preprocessor,
)

from .common import get_strict_level_map


if six.PY2:
    reload(sys)  # noqa: W0602
    sys.setdefaultencoding("utf-8")


dateutil = pytest.importorskip("dateutil", minversion="2.7")

DATATIME_DATA = datetime.datetime(2017, 1, 2, 3, 4, 5)

nan = float("nan")
inf = float("inf")


class Test_DataPeroperty_eq(object):
    @pytest.mark.parametrize(
        ["lhs", "rhs", "expected"],
        [
            [1, 1, True],
            [1, 2, False],
            [1, 0.1, False],
            [1, True, False],
            [1.1, 1.1, True],
            [1, nan, False],
            [nan, nan, True],
            [None, None, True],
        ],
    )
    def test_normal(self, lhs, rhs, expected):
        lhs = DataProperty(lhs)
        rhs = DataProperty(rhs)

        assert (lhs == rhs) == expected
        assert (lhs != rhs) == (not expected)


class Test_DataPeroperty_data_typecode(object):
    @pytest.mark.parametrize(
        ["value", "expected_data", "expected_typecode"],
        [["-0.00284241876820074", Decimal("-0.00284241876820074"), Typecode.REAL_NUMBER]],
    )
    def test_normal(self, value, expected_data, expected_typecode):
        dp = DataProperty(value)

        assert dp == dp
        assert dp.data == expected_data
        assert dp.typecode == expected_typecode

    @pytest.mark.parametrize(
        ["value", "is_convert", "expected_data", "expected_typecode"],
        [
            [1.0, True, 1, Typecode.INTEGER],
            [six.MAXSIZE, True, six.MAXSIZE, Typecode.INTEGER],
            [-six.MAXSIZE, False, -six.MAXSIZE, Typecode.INTEGER],
            [text_type(-six.MAXSIZE), True, -six.MAXSIZE, Typecode.INTEGER],
            [text_type(six.MAXSIZE), False, text_type(six.MAXSIZE), Typecode.STRING],
            [1.1, True, 1, Typecode.INTEGER],
            [-1.1, False, Decimal("-1.1"), Typecode.REAL_NUMBER],
            [Decimal("1.1"), False, Decimal("1.1"), Typecode.REAL_NUMBER],
            ["1.1", True, 1, Typecode.INTEGER],
            ["-1.1", False, "-1.1", Typecode.STRING],
            ["a", True, "a", Typecode.STRING],
            ["a", False, "a", Typecode.STRING],
            ["", True, "", Typecode.NULL_STRING],
            ["", False, "", Typecode.NULL_STRING],
            [" ", True, "", Typecode.NULL_STRING],
            [" ", False, "", Typecode.NULL_STRING],
            ["3.3.5", True, "3.3.5", Typecode.STRING],
            ["51.0.2704.106", True, "51.0.2704.106", Typecode.STRING],
            [True, True, 1, Typecode.INTEGER],
            [False, False, False, Typecode.BOOL],
            ["100-0002", False, "100-0002", Typecode.STRING],
            ["127.0.0.1", True, ipaddress.IPv4Address("127.0.0.1"), Typecode.IP_ADDRESS],
            ["127.0.0.1", False, "127.0.0.1", Typecode.STRING],
            ["::1", True, ipaddress.IPv6Address("::1"), Typecode.IP_ADDRESS],
            ["::1", False, "::1", Typecode.STRING],
            [[], True, [], Typecode.LIST],
            [[], False, [], Typecode.LIST],
            [{}, True, {}, Typecode.DICTIONARY],
            [{}, False, {}, Typecode.DICTIONARY],
            [
                "2017-01-02 03:04:05",
                True,
                datetime.datetime(2017, 1, 2, 3, 4, 5),
                Typecode.DATETIME,
            ],
            [DATATIME_DATA, True, DATATIME_DATA, Typecode.DATETIME],
            ["2017-01-02 03:04:05", False, "2017-01-02 03:04:05", Typecode.STRING],
            [None, True, None, Typecode.NONE],
            [None, False, None, Typecode.NONE],
            ["None", True, "None", Typecode.STRING],
            ["None", False, "None", Typecode.STRING],
            [inf, True, inf, Typecode.INFINITY],
            [inf, False, Decimal(inf), Typecode.INFINITY],
            ["inf", True, Decimal(inf), Typecode.INFINITY],
            ["inf", False, "inf", Typecode.STRING],
            ["nan", False, "nan", Typecode.STRING],
            [
                "Høgskolen i Østfold er et eksempel...",
                True,
                "Høgskolen i Østfold er et eksempel...",
                Typecode.STRING,
            ],
            [
                "Høgskolen i Østfold er et eksempel...",
                False,
                "Høgskolen i Østfold er et eksempel...",
                Typecode.STRING,
            ],
            ["新しいテキスト ドキュメント.txt".encode("utf_8"), True, "新しいテキスト ドキュメント.txt", Typecode.STRING],
        ],
    )
    def test_normal_strict_map(self, value, is_convert, expected_data, expected_typecode):
        dp = DataProperty(value, strict_level_map=get_strict_level_map(not is_convert))

        assert dp == dp
        assert dp != DataProperty("test for __ne__")
        assert dp.data == expected_data
        assert dp.typecode == expected_typecode

    @pytest.mark.parametrize(
        ["value", "strip_str", "is_strict", "expected_data", "expected_typecode"],
        [
            ['"1"', '"', False, 1, Typecode.INTEGER],
            ['"1"', "", False, '"1"', Typecode.STRING],
            ['"1"', '"', True, "1", Typecode.STRING],
            ['"1"', "", False, '"1"', Typecode.STRING],
        ],
    )
    def test_normal_strip_str(self, value, strip_str, is_strict, expected_data, expected_typecode):
        dp = DataProperty(
            value,
            preprocessor=Preprocessor(strip_str=strip_str),
            strict_level_map=get_strict_level_map(is_strict),
        )

        assert dp.data == expected_data
        assert dp.typecode == expected_typecode

    @pytest.mark.parametrize(
        ["value", "type_hint", "strict_level", "expected_typecode"],
        [
            ["2017-01-02 03:04:05", None, StrictLevel.MIN, Typecode.DATETIME],
            ["2017-01-02 03:04:05", None, StrictLevel.MAX, Typecode.STRING],
            ["2017-01-02 03:04:05", DateTime, StrictLevel.MIN, Typecode.DATETIME],
            ["2017-01-02 03:04:05", DateTime, StrictLevel.MAX, Typecode.DATETIME],
            ["2017-01-02 03:04:05", Integer, StrictLevel.MIN, Typecode.DATETIME],
            ["2017-01-02 03:04:05", Integer, StrictLevel.MAX, Typecode.STRING],
            [DATATIME_DATA, None, StrictLevel.MIN, Typecode.DATETIME],
            [DATATIME_DATA, None, StrictLevel.MAX, Typecode.DATETIME],
            [DATATIME_DATA, String, StrictLevel.MIN, Typecode.STRING],
            [DATATIME_DATA, String, StrictLevel.MAX, Typecode.STRING],
            ["100-0002", None, StrictLevel.MIN, Typecode.STRING],
            ["45e76582", None, StrictLevel.MIN, Typecode.INTEGER],
            ["45e76582", None, StrictLevel.MAX, Typecode.STRING],
            ["4.5e-4", None, StrictLevel.MIN, Typecode.INTEGER],
            ["4.5e-4", None, StrictLevel.MIN + 1, Typecode.REAL_NUMBER],
            ["4.5e-4", None, StrictLevel.MAX, Typecode.STRING],
            [1, String, StrictLevel.MAX, Typecode.STRING],
            [1, String, StrictLevel.MIN, Typecode.STRING],
            [float("inf"), RealNumber, StrictLevel.MAX, Typecode.INFINITY],
            [float("inf"), RealNumber, StrictLevel.MIN, Typecode.INFINITY],
            [1, RealNumber, StrictLevel.MAX, Typecode.INTEGER],
            [1, RealNumber, StrictLevel.MIN, Typecode.INTEGER],
            [1.1, Integer, StrictLevel.MAX, Typecode.INTEGER],
            [1.1, Integer, StrictLevel.MIN, Typecode.INTEGER],
            ["true", None, StrictLevel.MAX, Typecode.STRING],
            ["false", None, StrictLevel.MAX, Typecode.STRING],
            ["true", None, StrictLevel.MIN, Typecode.BOOL],
            ["false", None, StrictLevel.MIN, Typecode.BOOL],
            ["true", Bool, StrictLevel.MIN, Typecode.BOOL],
            ["false", Bool, StrictLevel.MIN, Typecode.BOOL],
        ],
    )
    def test_normal_type_hint(self, value, type_hint, strict_level, expected_typecode):
        dp = DataProperty(value, type_hint=type_hint, strict_level_map={"default": strict_level})

        assert dp.typecode == expected_typecode

    @pytest.mark.parametrize(
        ["value", "is_convert", "expected_data", "expected_typecode"],
        [
            [nan, True, nan, Typecode.NAN],
            [nan, False, nan, Typecode.NAN],
            ["nan", True, nan, Typecode.NAN],
        ],
    )
    def test_normal_nan(self, value, is_convert, expected_data, expected_typecode):
        dp = DataProperty(value, strict_level_map=get_strict_level_map(not is_convert))

        assert Nan(dp.data).is_type()
        assert dp.typecode == expected_typecode


class Test_DataPeroperty_to_str(object):
    @pytest.mark.parametrize(
        ["value", "type_hint", "is_strict", "expected_data", "expected_str"],
        [
            [float("inf"), None, True, Decimal("inf"), "Infinity"],
            [float("inf"), None, False, Decimal("inf"), "Infinity"],
            [float("inf"), RealNumber, True, Decimal("inf"), "Infinity"],
            [float("inf"), RealNumber, False, Decimal("inf"), "Infinity"],
            [float("inf"), String, False, "inf", "inf"],
        ],
    )
    def test_normal(self, value, type_hint, is_strict, expected_data, expected_str):
        dp = DataProperty(
            value, type_hint=type_hint, strict_level_map=get_strict_level_map(is_strict)
        )

        assert dp.data == expected_data
        assert dp.to_str() == expected_str

    @pytest.mark.parametrize(
        ["value", "format_flags", "expected"], [[1234567, Format.THOUSAND_SEPARATOR, "1,234,567"]]
    )
    def test_normal_format_str(self, value, format_flags, expected):
        dp = DataProperty(value, format_flags=format_flags)

        assert dp.to_str() == expected


class Test_DataPeroperty_set_data(object):
    @pytest.mark.parametrize(
        ["value", "is_convert", "replace_tabs_with_spaces", "tab_length", "expected"],
        [
            ["a\tb", True, True, 2, "a  b"],
            ["\ta\t\tb\tc\t", True, True, 2, "  a    b  c  "],
            ["a\tb", True, True, 4, "a    b"],
            ["a\tb", True, False, 4, "a\tb"],
            ["a\tb", True, True, None, "a\tb"],
        ],
    )
    def test_normal_tab(self, value, is_convert, replace_tabs_with_spaces, tab_length, expected):
        dp = DataProperty(
            value,
            preprocessor=Preprocessor(
                replace_tabs_with_spaces=replace_tabs_with_spaces, tab_length=tab_length,
            ),
            strict_level_map=get_strict_level_map(not is_convert),
        )

        assert dp.data == expected


class Test_DataPeroperty_is_escape_html_tag(object):
    @pytest.mark.skipif("six.PY2")
    @pytest.mark.parametrize(
        ["value", "is_escape_html_tag", "expected"],
        [
            [
                "<a href='https://google.com'>test</a>",
                True,
                "&lt;a href=&#x27;https://google.com&#x27;&gt;test&lt;/a&gt;",
            ],
            [
                "<a href='https://google.com'>test</a>",
                False,
                "<a href='https://google.com'>test</a>",
            ],
            [True, True, True],
        ],
    )
    def test_normal_tab(self, value, is_escape_html_tag, expected):
        dp = DataProperty(value, preprocessor=Preprocessor(is_escape_html_tag=is_escape_html_tag))

        assert dp.data == expected


class Test_DataPeroperty_float_type(object):
    @pytest.mark.parametrize(
        ["value", "float_type", "expected"], [[1.1, float, 1.1], [1.1, Decimal, Decimal("1.1")]]
    )
    def test_normal_tab(self, value, float_type, expected):
        dp = DataProperty(value, float_type=float_type)

        assert isinstance(dp.data, float_type)
        assert dp.data == expected


class Test_DataPeroperty_align(object):
    @pytest.mark.parametrize(
        ["value", "expected"],
        [
            [1, Align.RIGHT],
            [1.1, Align.RIGHT],
            ["a", Align.LEFT],
            [True, Align.LEFT],
            [DATATIME_DATA, Align.LEFT],
            [None, Align.LEFT],
            [inf, Align.LEFT],
            [nan, Align.LEFT],
        ],
    )
    def test_normal(self, value, expected):
        dp = DataProperty(value)
        assert dp.align == expected


class Test_DataPeroperty_len(object):
    @pytest.mark.parametrize(
        ["value", "expected_acw", "expected_len"],
        [
            [1, 1, None],
            [-1, 2, None],
            [1.0, 1, None],
            [-1.0, 2, None],
            [1.1, 3, None],
            [-1.1, 4, None],
            [12.34, 5, None],
            ["000", 1, None],
            ["123456789", 9, None],
            ["-123456789", 10, None],
            ["45e76582", 8, 8],
            ["a", 1, 1],
            ["a" * 1000, 1000, 1000],
            ["あ", 2, 1],
            [True, 4, None],
            [None, 4, None],
            [inf, 8, None],
            [nan, 3, None],
        ],
    )
    def test_normal(self, value, expected_acw, expected_len):
        dp = DataProperty(value)

        assert dp.ascii_char_width == expected_acw
        assert dp.length == expected_len

    @pytest.mark.parametrize(
        ["value", "expected_acw", "expected_len"],
        [
            [colored(0, "red"), 1, 10],
            [colored(12.34, "red"), 5, 14],
            [colored("abc", "green"), 3, 12],
        ],
    )
    def test_normal_ascii_escape_sequence(self, value, expected_acw, expected_len):
        dp = DataProperty(value)

        assert dp.ascii_char_width == expected_acw
        assert dp.length == expected_len

    @pytest.mark.parametrize(
        ["value", "eaaw", "expected_acw", "expected_len"], [["øø", 1, 2, 2], ["øø", 2, 4, 2]]
    )
    def test_normal_eaaw(self, value, eaaw, expected_acw, expected_len):
        dp = DataProperty(value, east_asian_ambiguous_width=eaaw)

        assert dp.ascii_char_width == expected_acw
        assert dp.length == expected_len

    @pytest.mark.parametrize(["value", "expected"], [[nan, nan]])
    def test_abnormal(self, value, expected):
        Nan(DataProperty(value).length).is_type()

    @pytest.mark.parametrize(
        ["value", "eaaw", "expected"],
        [["øø", None, ValueError], ["øø", 0, ValueError], ["øø", 3, ValueError]],
    )
    def test_exception_eaaw(self, value, eaaw, expected):
        with pytest.raises(expected):
            DataProperty(value, east_asian_ambiguous_width=eaaw).ascii_char_width


class Test_DataPeroperty_is_include_ansi_escape(object):
    @pytest.mark.parametrize(
        ["value", "expected_acw"],
        [
            [0, False],
            [colored(0, "red"), True],
            [12.34, False],
            [colored(12.34, "red"), True],
            ["abc", False],
            [colored("abc", "green"), True],
        ],
    )
    def test_normal(self, value, expected_acw):
        assert DataProperty(value).is_include_ansi_escape == expected_acw


class Test_DataPeroperty_line_break_handling(object):
    @pytest.mark.parametrize(
        ["value", "line_break_handling", "expected"],
        [
            ["a\nb", LineBreakHandling.NOP, "a\nb"],
            ["a\nb", LineBreakHandling.REPLACE, "a b"],
            ["a\nb", LineBreakHandling.ESCAPE, "a\\nb"],
            ["a\r\nb", LineBreakHandling.ESCAPE, "a\\r\\nb"],
            [123, LineBreakHandling.ESCAPE, 123],
        ],
    )
    def test_normal(self, value, line_break_handling, expected):
        assert (
            DataProperty(
                value, preprocessor=Preprocessor(line_break_handling=line_break_handling)
            ).data
            == expected
        )


class Test_DataPeroperty_get_padding_len(object):
    @pytest.mark.skipif("six.PY2")
    @pytest.mark.parametrize(
        ["value", "ascii_char_width", "expected"],
        [
            [1, 8, 8],
            ["000", 8, 8],
            ["a" * 1000, 8, 8],
            ["あ", 8, 7],
            ["あ" * 100, 8, 0],
            ["いろは", 8, 5],
            [["side", "where"], 20, 20],
            [["い" * 100, "ろは"], 8, 0],
            [["い", "ろは"], 20, 17],
        ],
    )
    def test_normal(self, value, ascii_char_width, expected):
        assert DataProperty(value).get_padding_len(ascii_char_width) == expected

    @pytest.mark.parametrize(
        ["value", "ascii_char_width", "ambiguous_width", "expected"],
        [["aøb", 4, 1, 4], ["aøb", 4, 2, 3]],
    )
    def test_normal_east_asian_ambiguous_width(
        self, value, ascii_char_width, ambiguous_width, expected
    ):
        dp = DataProperty(value, east_asian_ambiguous_width=ambiguous_width)
        assert dp.get_padding_len(ascii_char_width) == expected


class Test_DataPeroperty_integer_digits(object):
    @pytest.mark.parametrize(["value", "expected"], [[1, 1], [1.0, 1], [12.34, 2]])
    def test_normal(self, value, expected):
        dp = DataProperty(value)
        assert dp.integer_digits == expected

    @pytest.mark.parametrize(["value"], [[None], [True], [DATATIME_DATA], ["a"], [inf], [nan]])
    def test_abnormal(self, value):
        dp = DataProperty(value)
        Nan(dp.integer_digits).is_type()


class Test_DataPeroperty_decimal_places(object):
    @pytest.mark.parametrize(["value", "expected"], [[1, 0], [1.0, 0], [1.1, 1], [12.34, 2]])
    def test_normal(self, value, expected):
        dp = DataProperty(value)
        assert dp.decimal_places == expected

    @pytest.mark.parametrize(["value"], [[None], [True], [DATATIME_DATA], ["a"], [inf], [nan]])
    def test_abnormal(self, value):
        dp = DataProperty(value)
        Nan(dp.decimal_places).is_type()


class Test_DataPeroperty_additional_format_len(object):
    @pytest.mark.parametrize(
        ["value", "expected"],
        [
            [2147483648, 0],
            [0, 0],
            [-1, 1],
            [-0.01, 1],
            ["2147483648", 0],
            ["1", 0],
            ["-1", 1],
            ["-0.01", 1],
            [None, 0],
            [True, 0],
            [DATATIME_DATA, 0],
            ["a", 0],
            [inf, 0],
            [nan, 0],
        ],
    )
    def test_normal(self, value, expected):
        dp = DataProperty(value)
        assert dp.additional_format_len == expected


class Test_DataPeroperty_repr(object):
    @pytest.mark.parametrize(
        ["value", "strict_level_map", "expected"],
        [
            ["100-0004", MIN_STRICT_LEVEL_MAP, 75],
            [{"a": 1}, DefaultValue.STRICT_LEVEL_MAP, 75],
            ["新しいテキスト ドキュメント.txt", DefaultValue.STRICT_LEVEL_MAP, 80],
        ],
    )
    def test_smoke(self, value, strict_level_map, expected):
        dp = DataProperty(value, strict_level_map=strict_level_map)
        assert len(dp.__repr__()) > expected

    @pytest.mark.skipif("six.PY2")
    @pytest.mark.parametrize(
        ["value", "strict_level_map", "expected"],
        [
            [
                0,
                DefaultValue.STRICT_LEVEL_MAP,
                "data=0, type=INTEGER, align=right, "
                "ascii_width=1, int_digits=1, decimal_places=0, extra_len=0",
            ],
            [
                colored(0, "red"),
                DefaultValue.STRICT_LEVEL_MAP,
                (
                    ("data={}, type=STRING, align=right, ".format(colored(0, "red")))
                    + "ascii_width=1, length=10, int_digits=1, decimal_places=0, "
                    + "extra_len=0"
                ),
            ],
            [
                -1.0,
                DefaultValue.STRICT_LEVEL_MAP,
                "data=-1, type=INTEGER, align=right, "
                "ascii_width=2, int_digits=1, decimal_places=0, extra_len=1",
            ],
            [
                -1.1,
                DefaultValue.STRICT_LEVEL_MAP,
                "data=-1.1, type=REAL_NUMBER, align=right, "
                "ascii_width=4, int_digits=1, decimal_places=1, extra_len=1",
            ],
            [
                -12.234,
                DefaultValue.STRICT_LEVEL_MAP,
                "data=-12.23, type=REAL_NUMBER, align=right, "
                "ascii_width=6, int_digits=2, decimal_places=2, extra_len=1",
            ],
            [
                0.01,
                DefaultValue.STRICT_LEVEL_MAP,
                "data=0.01, type=REAL_NUMBER, align=right, "
                "ascii_width=4, int_digits=1, decimal_places=2, extra_len=0",
            ],
            [
                "abcdefg",
                DefaultValue.STRICT_LEVEL_MAP,
                "data=abcdefg, type=STRING, align=left, ascii_width=7, length=7, extra_len=0",
            ],
            [
                "いろは",
                DefaultValue.STRICT_LEVEL_MAP,
                "data=いろは, type=STRING, align=left, ascii_width=6, length=3, extra_len=0",
            ],
            [
                None,
                DefaultValue.STRICT_LEVEL_MAP,
                "data=None, type=NONE, align=left, ascii_width=4, extra_len=0",
            ],
            [
                True,
                DefaultValue.STRICT_LEVEL_MAP,
                "data=True, type=BOOL, align=left, ascii_width=4, extra_len=0",
            ],
            [
                DATATIME_DATA,
                DefaultValue.STRICT_LEVEL_MAP,
                "data=2017-01-02 03:04:05, type=DATETIME, align=left, "
                "ascii_width=19, extra_len=0",
            ],
            [
                "2017-01-02 03:04:05",
                DefaultValue.STRICT_LEVEL_MAP,
                "data=2017-01-02 03:04:05, type=STRING, align=left, "
                "ascii_width=19, length=19, extra_len=0",
            ],
            [
                "2017-01-02 03:04:05+0900",
                MIN_STRICT_LEVEL_MAP,
                "data=2017-01-02 03:04:05+09:00, type=DATETIME, align=left, "
                "ascii_width=24, extra_len=0",
            ],
            [
                inf,
                DefaultValue.STRICT_LEVEL_MAP,
                "data=Infinity, type=INFINITY, align=left, ascii_width=8, extra_len=0",
            ],
            [
                nan,
                DefaultValue.STRICT_LEVEL_MAP,
                "data=NaN, type=NAN, align=left, ascii_width=3, extra_len=0",
            ],
            [
                ["side", "where"],
                DefaultValue.STRICT_LEVEL_MAP,
                "data=['side', 'where'], type=LIST, align=left, "
                "ascii_width=17, length=2, extra_len=0",
            ],
            [
                ["い", "ろは"],
                DefaultValue.STRICT_LEVEL_MAP,
                "data=['い', 'ろは'], type=LIST, align=left, ascii_width=14, length=2, extra_len=0",
            ],
        ],
    )
    def test_normal(self, value, strict_level_map, expected):
        dp = DataProperty(value, strict_level_map=strict_level_map)

        print("[expected] {}".format(expected))
        print("[actual]   {}".format(dp))

        assert text_type(dp) == expected
