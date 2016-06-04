# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <gogogo.vm@gmail.com>
"""

import datetime
from dateutil.tz import tzoffset
import pytest

from dataproperty import DateTimeConverter


class Test_DateTimeConverter_to_datetime:

    @pytest.mark.parametrize(["value", "expected"], [
        [
            "2017-03-22T10:00:00+0900",
            datetime.datetime(2017, 3, 22, 10, 0, tzinfo=tzoffset(None, 32400))
        ],
        [None, None],
        [11111, None],
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
        ["invalid time string", ValueError],
    ])
    def test_exception(self, value, expected):
        dt_converter = DateTimeConverter(value)

        with pytest.raises(expected):
            dt_converter.to_datetime()
