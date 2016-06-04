# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <gogogo.vm@gmail.com>
"""

import datetime
from dateutil.tz import tzoffset
import pytest
import six

from dataproperty import DateTimeConverter
from dataproperty import TypeConversionError
from dataproperty import convert_value
from dataproperty import is_nan


nan = float("nan")
inf = float("inf")


class Test_DateTimeConverter_to_datetime:

    @pytest.mark.parametrize(["value", "expected"], [
        [
            datetime.datetime(
                2017, 3, 22, 10, 0, tzinfo=tzoffset(None, 32400)),
            datetime.datetime(
                2017, 3, 22, 10, 0, tzinfo=tzoffset(None, 32400)),
        ],
        [
            "2017-03-22T10:00:00+0900",
            datetime.datetime(2017, 3, 22, 10, 0, tzinfo=tzoffset(None, 32400))
        ],
    ])
    def test_normal(self, value, expected):
        dt_converter = DateTimeConverter(value)

        assert dt_converter.to_datetime() == expected

    @pytest.mark.parametrize(["value", "expected"], [
        [
            "2015-03-08T00:00:00-0400",
            "2015-03-08 00:00:00-04:00",
        ],
        [
            "2015-03-08T12:00:00-0400",
            "2015-03-08 12:00:00-03:00",
        ],
        [
            "2015-03-08T00:00:00-0800",
            "2015-03-08 00:00:00-08:00",
        ],
        [
            "2015-03-08T12:00:00-0800",
            "2015-03-08 12:00:00-07:00",
        ],
    ])
    def test_normal_dst(self, value, expected):
        dt_converter = DateTimeConverter(value)

        assert str(dt_converter) == expected
        assert str(dt_converter.to_datetime()) == expected

    @pytest.mark.parametrize(["value", "expected"], [
        ["invalid time string", TypeConversionError],
        [None, TypeConversionError],
        [11111, TypeConversionError],
    ])
    def test_exception(self, value, expected):
        dt_converter = DateTimeConverter(value)

        with pytest.raises(expected):
            dt_converter.to_datetime()


class Test_convert_value:

    @pytest.mark.parametrize(["value", "expected"], [
        ["0", 0],
        [str(six.MAXSIZE), six.MAXSIZE],
        [str(-six.MAXSIZE), -six.MAXSIZE],
        [0, 0],
        [six.MAXSIZE, six.MAXSIZE],
        [-six.MAXSIZE, -six.MAXSIZE],

        ["0.0", 0],
        [0.0, 0],

        ["aaaaa", "aaaaa"],

        [inf, inf],
    ])
    def test_normal(self, value, expected):
        assert convert_value(value) == expected

    @pytest.mark.parametrize(["value", "none_return_value", "expected"], [
        [None, None, None],
        ["1", None, 1],
        [None, "null", "null"],
        ["1", "null", 1],
    ])
    def test_none(self, value, none_return_value, expected):
        assert convert_value(value, none_return_value) == expected

    def test_abnormal(self):
        assert is_nan(convert_value(nan))
