# encoding: utf-8

from __future__ import unicode_literals

import pytest
from typepy import Typecode

from dataproperty import Format
from dataproperty._common import DefaultValue
from dataproperty._formatter import Formatter


dt_format = DefaultValue.DATETIME_FORMAT


class TestFormatter_make_format_str(object):
    @pytest.mark.parametrize(
        ["format_flags", "datetime_format_str", "decimal_places", "typecode", "expected"],
        [
            [None, dt_format, None, Typecode.STRING, "{:s}"],
            [Format.THOUSAND_SEPARATOR, dt_format, None, Typecode.STRING, "{:s}"],
            [None, dt_format, None, Typecode.INTEGER, "{:d}"],
            [Format.THOUSAND_SEPARATOR, dt_format, None, Typecode.INTEGER, "{:,d}"],
            [None, dt_format, 2, Typecode.INTEGER, "{:d}"],
            [None, dt_format, None, Typecode.REAL_NUMBER, "{:f}"],
            [Format.THOUSAND_SEPARATOR, dt_format, None, Typecode.REAL_NUMBER, "{:,f}"],
            [Format.THOUSAND_SEPARATOR, dt_format, 2, Typecode.REAL_NUMBER, "{:,.2f}"],
            [None, dt_format, 2, Typecode.REAL_NUMBER, "{:.2f}"],
            [None, dt_format, None, Typecode.INFINITY, "{:f}"],
            [None, dt_format, None, Typecode.NAN, "{:f}"],
            [None, dt_format, None, Typecode.DATETIME, "{:%Y-%m-%dT%H:%M:%S%z}"],
            [None, "%Y-%m-%d", None, Typecode.DATETIME, "{:%Y-%m-%d}"],
            [None, None, None, Typecode.NONE, "{}"],
            [None, None, None, Typecode.IP_ADDRESS, "{}"],
            [None, None, None, Typecode.BOOL, "{}"],
            [None, None, None, Typecode.DICTIONARY, "{}"],
            [None, None, None, Typecode.LIST, "{}"],
        ],
    )
    def test_normal(self, format_flags, datetime_format_str, decimal_places, typecode, expected):
        formatter = Formatter(format_flags=format_flags, datetime_format_str=datetime_format_str)

        assert formatter.make_format_str(typecode, decimal_places) == expected


class TestFormatter_make_format_map(object):
    @pytest.mark.parametrize(
        ["format_flags", "datetime_format_str", "decimal_places", "expected"],
        [[None, dt_format, "", {}]],
    )
    def test_normal(self, format_flags, datetime_format_str, decimal_places, expected):
        formatter = Formatter(format_flags=format_flags, datetime_format_str=datetime_format_str)

        assert formatter.make_format_map(decimal_places) == {
            Typecode.INTEGER: "{:d}",
            Typecode.REAL_NUMBER: "{:f}",
            Typecode.INFINITY: "{:f}",
            Typecode.NAN: "{:f}",
            Typecode.DATETIME: "{:%Y-%m-%dT%H:%M:%S%z}",
            Typecode.NONE: "{}",
            Typecode.IP_ADDRESS: "{}",
            Typecode.BOOL: "{}",
            Typecode.DICTIONARY: "{}",
            Typecode.LIST: "{}",
        }
