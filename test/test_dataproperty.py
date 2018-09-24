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
from dataproperty import NOT_STRICT_TYPE_MAPPING, Align, DataProperty, DefaultValue
from six import text_type
from typepy import Bool, DateTime, Integer, Nan, RealNumber, String, Typecode

from .common import get_strict_type_mapping


if six.PY2:
    reload(sys)  # noqa: W0602
    sys.setdefaultencoding("utf-8")


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
            # [1.0, False, 1, Typecode.INTEGER],
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
    def test_normal_strict_mapping(self, value, is_convert, expected_data, expected_typecode):
        dp = DataProperty(value, strict_type_mapping=get_strict_type_mapping(not is_convert))

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
            value, strip_str=strip_str, strict_type_mapping=get_strict_type_mapping(is_strict)
        )

        assert dp.data == expected_data
        assert dp.typecode == expected_typecode

    @pytest.mark.parametrize(
        ["value", "type_hint", "is_strict", "expected_typecode"],
        [
            ["2017-01-02 03:04:05", None, False, Typecode.DATETIME],
            ["2017-01-02 03:04:05", None, True, Typecode.STRING],
            ["2017-01-02 03:04:05", DateTime, False, Typecode.DATETIME],
            ["2017-01-02 03:04:05", DateTime, True, Typecode.DATETIME],
            ["2017-01-02 03:04:05", Integer, False, Typecode.DATETIME],
            ["2017-01-02 03:04:05", Integer, True, Typecode.STRING],
            [DATATIME_DATA, None, False, Typecode.DATETIME],
            [DATATIME_DATA, None, True, Typecode.DATETIME],
            [DATATIME_DATA, String, False, Typecode.STRING],
            [DATATIME_DATA, String, True, Typecode.STRING],
            ["100-0002", None, False, Typecode.STRING],
            [1, String, True, Typecode.STRING],
            [1, String, False, Typecode.STRING],
            [float("inf"), RealNumber, True, Typecode.INFINITY],
            [float("inf"), RealNumber, False, Typecode.INFINITY],
            [1, RealNumber, True, Typecode.INTEGER],
            [1, RealNumber, False, Typecode.INTEGER],
            [1.1, Integer, True, Typecode.INTEGER],
            [1.1, Integer, False, Typecode.INTEGER],
            ["true", Bool, False, Typecode.BOOL],
            ["false", Bool, False, Typecode.BOOL],
        ],
    )
    def test_normal_type_hint(self, value, type_hint, is_strict, expected_typecode):

        dp = DataProperty(
            value, type_hint=type_hint, strict_type_mapping=get_strict_type_mapping(is_strict)
        )

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
        dp = DataProperty(value, strict_type_mapping=get_strict_type_mapping(not is_convert))

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
            value, type_hint=type_hint, strict_type_mapping=get_strict_type_mapping(is_strict)
        )

        assert dp.data == expected_data
        assert dp.to_str() == expected_str


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
            strict_type_mapping=get_strict_type_mapping(not is_convert),
            replace_tabs_with_spaces=replace_tabs_with_spaces,
            tab_length=tab_length,
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
        ],
    )
    def test_normal_tab(self, value, is_escape_html_tag, expected):
        dp = DataProperty(value, is_escape_html_tag=is_escape_html_tag)

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
        ["value", "expected_acs", "expected_len"],
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
            ["a", 1, 1],
            ["a" * 1000, 1000, 1000],
            ["あ", 2, 1],
            [True, 4, None],
            [None, 4, None],
            [inf, 8, None],
            [nan, 3, None],
        ],
    )
    def test_normal(self, value, expected_acs, expected_len):
        dp = DataProperty(value)

        assert dp.ascii_char_width == expected_acs
        assert dp.length == expected_len

    @pytest.mark.parametrize(
        ["value", "eaaw", "expected_acs", "expected_len"], [["øø", 1, 2, 2], ["øø", 2, 4, 2]]
    )
    def test_normal_eaaw(self, value, eaaw, expected_acs, expected_len):
        dp = DataProperty(value, east_asian_ambiguous_width=eaaw)

        assert dp.ascii_char_width == expected_acs
        assert dp.length == expected_len

    @pytest.mark.parametrize(["value", "expected"], [[nan, nan]])
    def test_abnormal(self, value, expected):
        dp = DataProperty(value)
        Nan(dp.length).is_type()

    @pytest.mark.parametrize(
        ["value", "eaaw", "expected"],
        [["øø", None, ValueError], ["øø", 0, ValueError], ["øø", 3, ValueError]],
    )
    def test_exception_eaaw(self, value, eaaw, expected):
        with pytest.raises(expected):
            DataProperty(value, east_asian_ambiguous_width=eaaw).ascii_char_width


class Test_DataPeroperty_get_padding_len(object):
    @pytest.mark.skipif('six.PY2')
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
        ["value", "strict_type_mapping", "expected"],
        [
            ["100-0004", NOT_STRICT_TYPE_MAPPING, 95],
            [{"a": 1}, DefaultValue.STRICT_LEVEL_MAPPING, 100],
            ["新しいテキスト ドキュメント.txt", DefaultValue.STRICT_LEVEL_MAPPING, 100],
        ],
    )
    def test_smoke(self, value, strict_type_mapping, expected):
        dp = DataProperty(value, strict_type_mapping=strict_type_mapping)
        assert len(dp.__repr__()) > expected

    @pytest.mark.skipif('six.PY2')
    @pytest.mark.parametrize(
        ["value", "strict_type_mapping", "expected"],
        [
            [
                0,
                DefaultValue.STRICT_LEVEL_MAPPING,
                "data=0, typename=INTEGER, align=right, "
                "ascii_char_width=1, "
                "integer_digits=1, decimal_places=0, additional_format_len=0",
            ],
            [
                -1.0,
                DefaultValue.STRICT_LEVEL_MAPPING,
                "data=-1, typename=INTEGER, align=right, "
                "ascii_char_width=2, "
                "integer_digits=1, decimal_places=0, additional_format_len=1",
            ],
            [
                -1.1,
                DefaultValue.STRICT_LEVEL_MAPPING,
                "data=-1.1, typename=REAL_NUMBER, align=right, "
                "ascii_char_width=4, "
                "integer_digits=1, decimal_places=1, additional_format_len=1",
            ],
            [
                -12.234,
                DefaultValue.STRICT_LEVEL_MAPPING,
                "data=-12.23, typename=REAL_NUMBER, align=right, "
                "ascii_char_width=6, "
                "integer_digits=2, decimal_places=2, additional_format_len=1",
            ],
            [
                0.01,
                DefaultValue.STRICT_LEVEL_MAPPING,
                "data=0.01, typename=REAL_NUMBER, align=right, "
                "ascii_char_width=4, "
                "integer_digits=1, decimal_places=2, additional_format_len=0",
            ],
            [
                "abcdefg",
                DefaultValue.STRICT_LEVEL_MAPPING,
                "data=abcdefg, typename=STRING, align=left, "
                "ascii_char_width=7, length=7, additional_format_len=0",
            ],
            [
                "いろは",
                DefaultValue.STRICT_LEVEL_MAPPING,
                "data=いろは, typename=STRING, align=left, "
                "ascii_char_width=6, length=3, additional_format_len=0",
            ],
            [
                None,
                DefaultValue.STRICT_LEVEL_MAPPING,
                "data=None, typename=NONE, align=left, "
                "ascii_char_width=4, additional_format_len=0",
            ],
            [
                True,
                DefaultValue.STRICT_LEVEL_MAPPING,
                "data=True, typename=BOOL, align=left, "
                "ascii_char_width=4, additional_format_len=0",
            ],
            [
                DATATIME_DATA,
                DefaultValue.STRICT_LEVEL_MAPPING,
                "data=2017-01-02 03:04:05, typename=DATETIME, align=left, "
                "ascii_char_width=19, additional_format_len=0",
            ],
            [
                "2017-01-02 03:04:05",
                DefaultValue.STRICT_LEVEL_MAPPING,
                "data=2017-01-02 03:04:05, typename=STRING, align=left, "
                "ascii_char_width=19, length=19, additional_format_len=0",
            ],
            [
                "2017-01-02 03:04:05+0900",
                NOT_STRICT_TYPE_MAPPING,
                "data=2017-01-02 03:04:05+09:00, typename=DATETIME, align=left, "
                "ascii_char_width=24, additional_format_len=0",
            ],
            [
                inf,
                DefaultValue.STRICT_LEVEL_MAPPING,
                "data=Infinity, typename=INFINITY, align=left, "
                "ascii_char_width=8, additional_format_len=0",
            ],
            [
                nan,
                DefaultValue.STRICT_LEVEL_MAPPING,
                "data=NaN, typename=NAN, align=left, "
                "ascii_char_width=3, additional_format_len=0",
            ],
            [
                ["side", "where"],
                DefaultValue.STRICT_LEVEL_MAPPING,
                "data=['side', 'where'], typename=LIST, align=left, "
                "ascii_char_width=17, length=2, additional_format_len=0",
            ],
            [
                ["い", "ろは"],
                DefaultValue.STRICT_LEVEL_MAPPING,
                "data=['い', 'ろは'], typename=LIST, align=left, "
                "ascii_char_width=14, length=2, additional_format_len=0",
            ],
        ],
    )
    def test_normal(self, value, strict_type_mapping, expected):
        dp = DataProperty(value, strict_type_mapping=strict_type_mapping)

        print("[expected] {}".format(expected))
        print("[actual]   {}".format(dp))

        assert text_type(dp) == expected
