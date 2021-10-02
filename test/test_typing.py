"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

import pytest

from dataproperty.typing import (
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
    normalize_type_hint,
)


class Test_normalize_type_hint:
    @pytest.mark.parametrize(
        ["value", "expected"],
        [
            ["bool", Bool],
            ["datetime", DateTime],
            ["dict", Dictionary],
            ["dictionary", Dictionary],
            ["inf", Infinity],
            ["infinity", Infinity],
            ["int", Integer],
            ["int ", Integer],
            ["int_", Integer],
            ["integer", Integer],
            ["ip", IpAddress],
            ["ipaddr", IpAddress],
            ["ipaddress", IpAddress],
            ["list", List],
            ["nan", Nan],
            ["none", NoneType],
            ["nullstr", NullString],
            ["nullstring", NullString],
            ["float", RealNumber],
            ["realnumber", RealNumber],
            ["str", String],
            ["string", String],
            ["", None],
            [None, None],
        ],
    )
    def test_normal(self, value, expected):
        assert normalize_type_hint(value) == expected
