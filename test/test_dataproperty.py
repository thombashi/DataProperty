# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <gogogo.vm@gmail.com>
"""

from __future__ import unicode_literals
from __future__ import print_function
import datetime
from decimal import Decimal
import sys

import pytest
import six

from dataproperty import *

from .common import get_strict_type_mapping


if six.PY2:
    reload(sys)
    sys.setdefaultencoding('utf-8')


DATATIME_DATA = datetime.datetime(2017, 1, 2, 3, 4, 5)

nan = float("nan")
inf = float("inf")


class Test_DataPeroperty_data_typecode:

    @pytest.mark.parametrize(
        ["value", "is_convert", "expected_data", "expected_typecode"],
        [
            [six.MAXSIZE, True, six.MAXSIZE, Typecode.INTEGER],
            [-six.MAXSIZE, False, -six.MAXSIZE, Typecode.INTEGER],
            [str(-six.MAXSIZE), True, -six.MAXSIZE, Typecode.INTEGER],
            [str(six.MAXSIZE), False, str(six.MAXSIZE), Typecode.STRING],

            [1.1, True, Decimal("1.1"), Typecode.FLOAT],
            [-1.1, False, Decimal("-1.1"), Typecode.FLOAT],
            [Decimal("1.1"), False, Decimal("1.1"), Typecode.FLOAT],

            ["1.1", True, Decimal("1.1"), Typecode.FLOAT],
            ["-1.1", False, "-1.1", Typecode.STRING],
            ["a", True, "a", Typecode.STRING],
            ["a", False, "a", Typecode.STRING],

            ["", True, "", Typecode.NULL_STRING],
            ["", False, "", Typecode.NULL_STRING],
            [" ", True, "", Typecode.NULL_STRING],
            [" ", False, "", Typecode.NULL_STRING],

            ["3.3.5", True, "3.3.5", Typecode.STRING],
            ["51.0.2704.106", True, "51.0.2704.106", Typecode.STRING],

            [True, True, True, Typecode.BOOL],
            [False, False, False, Typecode.BOOL],

            ["100-0002", False, "100-0002", Typecode.STRING],

            [{}, True, {}, Typecode.DICTIONARY],
            [{}, False, {}, Typecode.DICTIONARY],

            [
                "2017-01-02 03:04:05",
                True,
                datetime.datetime(2017, 1, 2, 3, 4, 5),
                Typecode.DATETIME
            ],
            [
                DATATIME_DATA,
                True,
                DATATIME_DATA,
                Typecode.DATETIME
            ],
            [
                "2017-01-02 03:04:05",
                False,
                "2017-01-02 03:04:05",
                Typecode.STRING
            ],

            [None, True, None, Typecode.NONE],
            [None, False, None, Typecode.NONE],
            ["None", True, "None", Typecode.STRING],
            ["None", False, "None", Typecode.STRING],

            [inf, True, inf, Typecode.INFINITY],
            [inf, False, Decimal(inf), Typecode.INFINITY],
            ["inf", True, Decimal(inf), Typecode.INFINITY],
            ["inf", False, "inf", Typecode.STRING],

            ["nan", False, "nan", Typecode.STRING],

            ["Høgskolen i Østfold er et eksempel...", True,
                "Høgskolen i Østfold er et eksempel...", Typecode.STRING],
            ["Høgskolen i Østfold er et eksempel...", False,
                "Høgskolen i Østfold er et eksempel...", Typecode.STRING],
            ["新しいテキスト ドキュメント.txt".encode("utf_8"), True,
                "新しいテキスト ドキュメント.txt", Typecode.STRING]
        ]
    )
    def test_normal(self, value, is_convert, expected_data, expected_typecode):
        dp = DataProperty(
            value,
            strict_type_mapping=get_strict_type_mapping(not is_convert))

        assert dp.data == expected_data
        assert dp.typecode == expected_typecode

    @pytest.mark.parametrize(
        [
            "value", "strip_str", "is_strict",
            "expected_data", "expected_typecode"
        ],
        [
            ['"1"', '"', False, 1, Typecode.INTEGER],
            ['"1"', '', False, '"1"', Typecode.STRING],
            ['"1"', '"', True, "1", Typecode.STRING],
            ['"1"', '', False, '"1"', Typecode.STRING],
        ]
    )
    def test_normal_strip_str(
            self, value, strip_str, is_strict,
            expected_data, expected_typecode):
        dp = DataProperty(
            value,
            strip_str=strip_str,
            strict_type_mapping=get_strict_type_mapping(is_strict))

        assert dp.data == expected_data
        assert dp.typecode == expected_typecode

    @pytest.mark.parametrize(
        ["value", "type_hint", "is_strict", "expected_typecode"],
        [
            ["2017-01-02 03:04:05", None, False, Typecode.DATETIME],
            ["2017-01-02 03:04:05", None, True, Typecode.STRING],
            ["2017-01-02 03:04:05", DateTimeType, False, Typecode.DATETIME],
            ["2017-01-02 03:04:05", DateTimeType, True, Typecode.DATETIME],
            ["2017-01-02 03:04:05", IntegerType, False, Typecode.DATETIME],
            ["2017-01-02 03:04:05", IntegerType, True, Typecode.STRING],
            [DATATIME_DATA, None, False, Typecode.DATETIME],
            [DATATIME_DATA, None, True, Typecode.DATETIME],
            [DATATIME_DATA, StringType, False, Typecode.STRING],
            [DATATIME_DATA, StringType, True, Typecode.STRING],
            ["100-0002", None, False, Typecode.DATETIME],

            [1, StringType, True, Typecode.STRING],
            [1, StringType, False, Typecode.STRING],

            [1, FloatType, True, Typecode.FLOAT],
            [1, FloatType, False, Typecode.FLOAT],
            [float("inf"), FloatType, True, Typecode.INFINITY],
            [float("inf"), FloatType, False, Typecode.INFINITY],

            [1.1, IntegerType, True, Typecode.INTEGER],
            [1.1, IntegerType, False, Typecode.INTEGER],

            ["true", BoolType, False, Typecode.BOOL],
            ["false", BoolType, False, Typecode.BOOL],
        ]
    )
    def test_normal_type_hint(
            self, value, type_hint, is_strict, expected_typecode):
        dp = DataProperty(
            value, type_hint=type_hint,
            strict_type_mapping=get_strict_type_mapping(is_strict))

        assert dp.typecode == expected_typecode

    @pytest.mark.parametrize(
        ["value", "is_convert", "expected_data", "expected_typecode"],
        [
            [nan, True, nan, Typecode.NAN],
            [nan, False, nan, Typecode.NAN],
            ["nan", True, nan, Typecode.NAN],
        ]
    )
    def test_normal_nan(
            self, value, is_convert, expected_data, expected_typecode):
        dp = DataProperty(
            value,
            strict_type_mapping=get_strict_type_mapping(not is_convert))

        assert NanType(dp.data).is_type()
        assert dp.typecode == expected_typecode


class Test_DataPeroperty_to_str:

    @pytest.mark.parametrize(
        ["value", "type_hint", "is_strict", "expected_data", "expected_str"],
        [
            [float("inf"), None, True, Decimal("inf"), "Infinity"],
            [float("inf"), None, False, Decimal("inf"), "Infinity"],
            [float("inf"), FloatType, True, Decimal("inf"), "Infinity"],
            [float("inf"), FloatType, False, Decimal("inf"), "Infinity"],
            [float("inf"), StringType, False, "inf", "inf"],
        ])
    def test_normal(self, value, type_hint, is_strict, expected_data, expected_str):
        dp = DataProperty(
            value,
            type_hint=type_hint,
            strict_type_mapping=get_strict_type_mapping(is_strict))

        assert dp.data == expected_data
        assert dp.to_str() == expected_str


class Test_DataPeroperty_set_data:

    @pytest.mark.parametrize(
        [
            "value", "is_convert",
            "replace_tabs_with_spaces", "tab_length",
            "expected"
        ],
        [
            ["a\tb", True, True, 2, "a  b"],
            ["\ta\t\tb\tc\t", True, True, 2, "  a    b  c  "],
            ["a\tb", True, True, 4, "a    b"],
            ["a\tb", True, False, 4, "a\tb"],
            ["a\tb", True, True, None, "a\tb"],
        ])
    def test_normal_tab(
            self, value, is_convert,
            replace_tabs_with_spaces, tab_length, expected):
        dp = DataProperty(
            value,
            strict_type_mapping=get_strict_type_mapping(not is_convert),
            replace_tabs_with_spaces=replace_tabs_with_spaces,
            tab_length=tab_length)

        assert dp.data == expected


class Test_DataPeroperty_float_type:

    @pytest.mark.parametrize(
        ["value",  "float_type", "expected"],
        [
            [1.1, float, 1.1],
            [1.1, Decimal, Decimal("1.1")],
        ])
    def test_normal_tab(self, value, float_type, expected):
        dp = DataProperty(value, float_type=float_type)

        assert isinstance(dp.data, float_type)
        assert dp.data == expected


class Test_DataPeroperty_align:

    @pytest.mark.parametrize(["value", "expected"], [
        [1, Align.RIGHT],
        [1.1, Align.RIGHT],
        ["a", Align.LEFT],
        [True, Align.LEFT],
        [DATATIME_DATA, Align.LEFT],
        [None, Align.LEFT],
        [inf, Align.LEFT],
        [nan, Align.LEFT],
    ])
    def test_normal(self, value, expected):
        dp = DataProperty(value)
        assert dp.align == expected


class Test_DataPeroperty_str_len:

    @pytest.mark.parametrize(["value", "expected"], [
        [1, 1],
        [-1, 2],
        [1.0, 1],
        [-1.0, 2],
        [1.1, 3],
        [-1.1, 4],
        [12.34, 5],

        ["000", 1],
        ["123456789", 9],
        ["-123456789", 10],

        ["a", 1],
        ["a" * 1000, 1000],
        ["あ", 1],
        ["ø", 1],

        [True, 4],
        [None, 4],
        [inf, 8],
        [nan, 3],
    ])
    def test_normal(self, value, expected):
        dp = DataProperty(value)
        assert dp.str_len == expected

    @pytest.mark.parametrize(["value", "expected"], [
        [nan, nan],
    ])
    def test_abnormal(self, value, expected):
        dp = DataProperty(value)
        NanType(dp.str_len).is_type()


class Test_DataPeroperty_get_padding_len:

    @pytest.mark.parametrize(["value", "ascii_char_width", "expected"], [
        [1, 8, 8],
        ["000", 8, 8],

        ["a" * 1000, 8, 8],
        ["あ", 8, 7],
        ["いろは", 8, 5],
    ])
    def test_normal(self, value, ascii_char_width, expected):
        dp = DataProperty(value)
        assert dp.get_padding_len(ascii_char_width) == expected

    @pytest.mark.parametrize(
        ["value", "ascii_char_width", "ambiguous_width", "expected"],
        [
            ["aøb", 4, 1, 4],
            ["aøb", 4, 2, 3],
        ]
    )
    def test_normal_east_asian_ambiguous_width(
            self, value, ascii_char_width, ambiguous_width, expected):
        dp = DataProperty(value, east_asian_ambiguous_width=ambiguous_width)
        assert dp.get_padding_len(ascii_char_width) == expected


class Test_DataPeroperty_integer_digits:

    @pytest.mark.parametrize(["value", "expected"], [
        [1, 1],
        [1.0, 1],
        [12.34, 2],
    ])
    def test_normal(self, value, expected):
        dp = DataProperty(value)
        assert dp.integer_digits == expected

    @pytest.mark.parametrize(["value"], [
        [None],
        [True],
        [DATATIME_DATA],
        ["a"],
        [inf],
        [nan],
    ])
    def test_abnormal(self, value):
        dp = DataProperty(value)
        NanType(dp.integer_digits).is_type()


class Test_DataPeroperty_decimal_places:

    @pytest.mark.parametrize(["value", "expected"], [
        [1, 0],
        [1.0, 0],
        [1.1, 1],
        [12.34, 2],
    ])
    def test_normal(self, value, expected):
        dp = DataProperty(value)
        assert dp.decimal_places == expected

    @pytest.mark.parametrize(["value"], [
        [None],
        [True],
        [DATATIME_DATA],
        ["a"],
        [inf],
        [nan],
    ])
    def test_abnormal(self, value):
        dp = DataProperty(value)
        NanType(dp.decimal_places).is_type()


class Test_DataPeroperty_additional_format_len:

    @pytest.mark.parametrize(["value", "expected"], [
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
    ])
    def test_normal(self, value, expected):
        dp = DataProperty(value)
        assert dp.additional_format_len == expected


class Test_DataPeroperty_repr:

    @pytest.mark.parametrize(["value", "strict_type_mapping", "expected"], [
        [
            "100-0004",
            NOT_STRICT_TYPE_MAPPING,
            100
        ],
        [
            {"a": 1},
            DefaultValue.STRICT_TYPE_MAPPING,
            100
        ],
        [
            "新しいテキスト ドキュメント.txt",
            DefaultValue.STRICT_TYPE_MAPPING,
            100
        ],
    ])
    def test_smoke(self, value, strict_type_mapping, expected):
        dp = DataProperty(value, strict_type_mapping=strict_type_mapping)
        assert len(dp.__repr__()) > expected

    @pytest.mark.parametrize(["value", "strict_type_mapping", "expected"], [
        [
            0,
            DefaultValue.STRICT_TYPE_MAPPING,
            "data=0, typename=INTEGER, align=right, str_len=1, "
            "ascii_char_width=1, "
            "integer_digits=1, decimal_places=0, additional_format_len=0",
        ],
        [
            -1.0,
            DefaultValue.STRICT_TYPE_MAPPING,
            "data=-1, typename=INTEGER, align=right, str_len=2, "
            "ascii_char_width=2, "
            "integer_digits=1, decimal_places=0, additional_format_len=1",
        ],
        [
            -1.1,
            DefaultValue.STRICT_TYPE_MAPPING,
            "data=-1.1, typename=FLOAT, align=right, str_len=4, "
            "ascii_char_width=4, "
            "integer_digits=1, decimal_places=1, additional_format_len=1",
        ],
        [
            -12.234,
            DefaultValue.STRICT_TYPE_MAPPING,
            "data=-12.23, typename=FLOAT, align=right, str_len=6, "
            "ascii_char_width=6, "
            "integer_digits=2, decimal_places=2, additional_format_len=1",
        ],
        [
            0.01,
            DefaultValue.STRICT_TYPE_MAPPING,
            "data=0.01, typename=FLOAT, align=right, str_len=4, "
            "ascii_char_width=4, "
            "integer_digits=1, decimal_places=2, additional_format_len=0",
        ],
        [
            "abcdefg",
            DefaultValue.STRICT_TYPE_MAPPING,
            "data=abcdefg, typename=STRING, align=left, str_len=7, "
            "ascii_char_width=7, "
            "integer_digits=nan, decimal_places=nan, additional_format_len=0",
        ],
        [
            None,
            DefaultValue.STRICT_TYPE_MAPPING,
            "data=None, typename=NONE, align=left, str_len=4, "
            "ascii_char_width=4, "
            "integer_digits=nan, decimal_places=nan, additional_format_len=0",
        ],
        [
            True,
            DefaultValue.STRICT_TYPE_MAPPING,
            "data=True, typename=BOOL, align=left, str_len=4, "
            "ascii_char_width=4, "
            "integer_digits=nan, decimal_places=nan, additional_format_len=0",
        ],
        [
            DATATIME_DATA,
            DefaultValue.STRICT_TYPE_MAPPING,
            "data=2017-01-02 03:04:05, typename=DATETIME, align=left, str_len=19, "
            "ascii_char_width=19, "
            "integer_digits=nan, decimal_places=nan, additional_format_len=0",
        ],
        [
            "2017-01-02 03:04:05",
            DefaultValue.STRICT_TYPE_MAPPING,
            "data=2017-01-02 03:04:05, typename=STRING, align=left, str_len=19, "
            "ascii_char_width=19, "
            "integer_digits=nan, decimal_places=nan, additional_format_len=0",
        ],
        [
            "2017-01-02 03:04:05+0900",
            NOT_STRICT_TYPE_MAPPING,
            "data=2017-01-02 03:04:05+09:00, typename=DATETIME, align=left, str_len=24, "
            "ascii_char_width=24, "
            "integer_digits=nan, decimal_places=nan, additional_format_len=0",
        ],
        [
            inf,
            DefaultValue.STRICT_TYPE_MAPPING,
            "data=Infinity, typename=INFINITY, align=left, str_len=8, "
            "ascii_char_width=8, "
            "integer_digits=nan, decimal_places=nan, additional_format_len=0",
        ],
        [
            nan,
            DefaultValue.STRICT_TYPE_MAPPING,
            "data=NaN, typename=NAN, align=left, str_len=3, "
            "ascii_char_width=3, "
            "integer_digits=nan, decimal_places=nan, additional_format_len=0",
        ],
    ])
    def test_normal(self, value, strict_type_mapping, expected):
        dp = DataProperty(value, strict_type_mapping=strict_type_mapping)

        print("[expected] {}".format(expected))
        print("[actual]   {}".format(dp))

        assert str(dp) == expected
