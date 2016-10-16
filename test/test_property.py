# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <gogogo.vm@gmail.com>
"""

import datetime
from decimal import Decimal

import pytest
import six

from dataproperty import *


DATATIME_DATA = datetime.datetime(2017, 1, 2, 3, 4, 5)

nan = float("nan")
inf = float("inf")


class Test_DataPeroperty_data_typecode:

    @pytest.mark.parametrize(
        ["value", "is_convert", "expected_data", "expected_typecode"],
        [
            [six.MAXSIZE, True, six.MAXSIZE, Typecode.INT],
            [-six.MAXSIZE, False, -six.MAXSIZE, Typecode.INT],
            [str(-six.MAXSIZE), True, -six.MAXSIZE, Typecode.INT],
            [str(six.MAXSIZE), False, str(six.MAXSIZE), Typecode.STRING],
            ["1.1", True, Decimal("1.1"), Typecode.FLOAT],
            ["-1.1", False, "-1.1", Typecode.STRING],
            ["a", True, "a", Typecode.STRING],
            ["a", False, "a", Typecode.STRING],

            ["3.3.5", True, "3.3.5", Typecode.STRING],
            ["51.0.2704.106", True, "51.0.2704.106", Typecode.STRING],

            [True, True, True, Typecode.BOOL],
            [False, False, False, Typecode.BOOL],

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
            [inf, False, inf, Typecode.INFINITY],
            ["inf", True, inf, Typecode.INFINITY],
            ["inf", False, "inf", Typecode.STRING],

            ["nan", False, "nan", Typecode.STRING],
        ]
    )
    def test_normal(self, value, is_convert, expected_data, expected_typecode):
        dp = DataProperty(value, is_convert=is_convert)
        assert dp.data == expected_data
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
        dp = DataProperty(value, is_convert=is_convert)
        assert is_nan(dp.data)
        assert dp.typecode == expected_typecode

    @pytest.mark.parametrize(["value", "none_value", "expected"], [
        [None, None, None],
        [None, "null", "null"],
        [None, "", ""],
        [None, 0, 0],
    ])
    def test_none(self, value, none_value, expected):
        dp = DataProperty(value, none_value)
        assert dp.data == expected
        assert dp.typecode == Typecode.NONE


def bool_converter_test(value):
    if value:
        return "true value"

    return "false value"


def datetime_converter_tostr_0(value):
    return value.strftime("%Y-%m-%d %H:%M:%S%z")


def datetime_converter_tostr_1(value):
    return value.strftime("%Y/%m/%d %H:%M:%S")


def datetime_converter_test_raw(value):
    return value


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
            is_convert=is_convert,
            replace_tabs_with_spaces=replace_tabs_with_spaces,
            tab_length=tab_length)

        assert dp.data == expected

    @pytest.mark.parametrize(
        ["value", "none_value", "is_convert", "expected"],
        [
            [None, "NONE", True, "NONE"],
            [None, "NONE", False, "NONE"],
        ]
    )
    def test_special_none(
            self, value, none_value,  is_convert, expected):
        dp = DataProperty(
            value,
            none_value=none_value,
            is_convert=is_convert)

        assert dp.data == expected

    @pytest.mark.parametrize(
        ["value", "bool_converter", "is_convert", "expected"],
        [
            ["True", bool_converter_test, True, "true value"],
            ["False", bool_converter_test, True, "false value"],
            ["True", bool_converter_test, False, "True"],
        ]
    )
    def test_special_bool(
            self, value, bool_converter,  is_convert, expected):
        dp = DataProperty(
            value,
            bool_converter=bool_converter,
            is_convert=is_convert)

        assert dp.data == expected

    @pytest.mark.parametrize(
        [
            "value", "datetime_converter", "datetime_format_str",
            "is_convert", "expected",
        ],
        [
            [
                DATATIME_DATA, datetime_converter_tostr_0,
                "s",
                True, "2017-01-02 03:04:05",
            ],
            [
                "2017-01-01 00:00:00", datetime_converter_tostr_1,
                "s",
                True, "2017/01/01 00:00:00",
            ],
            [
                "2017-01-01 00:00:00", datetime_converter_test_raw,
                "%Y-%m-%dT%H:%M:%S",
                True, datetime.datetime(2017, 1, 1, 0, 0, 0),
            ],
            [
                "2017-01-01 00:00:00", datetime_converter_test_raw,
                "s",
                False, "2017-01-01 00:00:00",
            ],
        ]
    )
    def test_special_datetime(
            self, value, datetime_converter, datetime_format_str,
            is_convert, expected):
        dp = DataProperty(
            value,
            datetime_converter=datetime_converter,
            datetime_format_str=datetime_format_str,
            is_convert=is_convert)

        assert dp.data == expected

    @pytest.mark.parametrize(
        ["value", "inf_value", "is_convert", "expected"],
        [
            [inf, "Infinity", True, "Infinity"],
            [inf, "Infinity", False, "Infinity"],
            ["inf", "Infinity", True, "Infinity"],
            ["inf", "Infinity", False, "inf"],
        ]
    )
    def test_special_inf(
            self, value, inf_value, is_convert, expected):
        dp = DataProperty(
            value,
            inf_value=inf_value,
            is_convert=is_convert)

        assert dp.data == expected

    @pytest.mark.parametrize(
        ["value", "nan_value", "is_convert", "expected"],
        [
            [nan, "not a number", True, "not a number"],
            [nan, "not a number", False, "not a number"],
            ["nan", "not a number", True, "not a number"],
            ["nan", "not a number", False, "nan"],
        ]
    )
    def test_special_nan(
            self, value, nan_value, is_convert, expected):
        dp = DataProperty(
            value,
            nan_value=nan_value,
            is_convert=is_convert)

        assert dp.data == expected


class Test_DataPeroperty_align:

    @pytest.mark.parametrize(["value", "expected"], [
        [1, Align.RIGHT],
        [1.0, Align.RIGHT],
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
        [1.0, 3],
        [-1.0, 4],
        [12.34, 5],

        ["000", 1],
        ["123456789", 9],
        ["-123456789", 10],

        ["a", 1],
        [True, 4],
        [None, 4],
        [inf, 3],
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
        is_nan(dp.str_len)


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
        is_nan(dp.integer_digits)


class Test_DataPeroperty_decimal_places:

    @pytest.mark.parametrize(["value", "expected"], [
        [1, 0],
        [1.0, 1],
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
        is_nan(dp.decimal_places)


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

    @pytest.mark.parametrize(["value", "expected"], [
        [
            0,
            "data=0, typename=INTEGER, align=right, str_len=1, "
            "integer_digits=1, decimal_places=0, additional_format_len=0",
        ],
        [
            -1.0,
            "data=-1.0, typename=FLOAT, align=right, str_len=4, "
            "integer_digits=1, decimal_places=1, additional_format_len=1",
        ],
        [
            -12.234,
            "data=-12.23, typename=FLOAT, align=right, str_len=6, "
            "integer_digits=2, decimal_places=2, additional_format_len=1",
        ],
        [
            "abcdefg",
            "data=abcdefg, typename=STRING, align=left, str_len=7, "
            "integer_digits=nan, decimal_places=nan, additional_format_len=0",
        ],
        [
            None,
            "data=None, typename=NONE, align=left, str_len=4, "
            "integer_digits=nan, decimal_places=nan, additional_format_len=0",
        ],
        [
            True,
            "data=True, typename=BOOL, align=left, str_len=4, "
            "integer_digits=nan, decimal_places=nan, additional_format_len=0",
        ],
        [
            DATATIME_DATA,
            "data=2017-01-02 03:04:05, typename=DATETIME, align=left, str_len=19, "
            "integer_digits=nan, decimal_places=nan, additional_format_len=0",
        ],
        [
            "2017-01-02 03:04:05",
            "data=2017-01-02 03:04:05, typename=DATETIME, align=left, str_len=19, "
            "integer_digits=nan, decimal_places=nan, additional_format_len=0",
        ],
        [
            "2017-01-02 03:04:05+0900",
            "data=2017-01-02 03:04:05+09:00, typename=DATETIME, align=left, str_len=24, "
            "integer_digits=nan, decimal_places=nan, additional_format_len=0",
        ],
        [
            "2017-01-02 03:04:05+09:00",
            "data=2017-01-02 03:04:05+09:00, typename=DATETIME, align=left, str_len=24, "
            "integer_digits=nan, decimal_places=nan, additional_format_len=0",
        ],
        [
            inf,
            "data=inf, typename=INFINITY, align=left, str_len=3, "
            "integer_digits=nan, decimal_places=nan, additional_format_len=0",
        ],
        [
            nan,
            "data=nan, typename=NAN, align=left, str_len=3, "
            "integer_digits=nan, decimal_places=nan, additional_format_len=0",
        ],
    ])
    def test_normal(self, value, expected):
        dp = DataProperty(value)
        assert str(dp) == expected
