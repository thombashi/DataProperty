# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <gogogo.vm@gmail.com>
"""

from __future__ import unicode_literals
import datetime
from decimal import Decimal
from dateutil.tz import tzoffset
import pytest
import six

from dataproperty import TypeConversionError
import dataproperty._converter as dpcc
from dataproperty import *


nan = float("nan")
inf = float("inf")


class Test_NopConverter_convert:

    @pytest.mark.parametrize(["value", "expected"], [
        [None, None],
        [0, 0],
        [six.MAXSIZE, six.MAXSIZE],
        [False, False],
        ["test_string", "test_string"],
    ])
    def test_normal(self, value, expected):
        converter = dpcc.NopConverter(value)
        typeobj = NoneType(value)

        assert converter.convert() == expected
        assert converter.try_convert() == expected
        assert typeobj.convert() == expected
        assert typeobj.try_convert() == expected


class Test_StringConverter_convert:

    @pytest.mark.parametrize(["value", "expected"], [
        [None, "None"],
        [six.MAXSIZE, str(six.MAXSIZE)],
        [-six.MAXSIZE, str(-six.MAXSIZE)],
        [inf, "inf"],
        [nan, "nan"],
        [True, "True"],
        [datetime.datetime(2017, 1, 2, 3, 4, 5), "2017-01-02 03:04:05"],
        ["吾輩は猫である", "吾輩は猫である"],
        [
            "新しいテキスト ドキュメント.txt".encode("utf_8"),
            "新しいテキスト ドキュメント.txt",
        ]
    ])
    def test_normal(self, value, expected):
        converter = dpcc.StringConverter(value)
        typeobj = StringType(value)

        assert converter.convert() == expected
        assert converter.try_convert() == expected
        assert typeobj.convert() == expected
        assert typeobj.try_convert() == expected


class Test_IntegerConverter_convert:

    @pytest.mark.parametrize(["value", "expected"], [
        [six.MAXSIZE, six.MAXSIZE], [-six.MAXSIZE, -six.MAXSIZE],
        [0., 0], [0.1, 0], [.5, 0],
        [True, 1], [False, 0],
        [str(six.MAXSIZE), six.MAXSIZE],
        [str(-six.MAXSIZE), -six.MAXSIZE],
    ])
    def test_normal(self, value, expected):
        converter = dpcc.IntegerConverter(value)
        typeobj = IntegerType(value)

        assert converter.convert() == expected
        assert converter.try_convert() == expected
        assert typeobj.convert() == expected
        assert typeobj.try_convert() == expected

    @pytest.mark.parametrize(["value", "expected"], [
        ["", TypeConversionError],
        [None, TypeConversionError],
        ["test", TypeConversionError],
        ["0.0", TypeConversionError],
        ["0.1", TypeConversionError],
        ["-0.1", TypeConversionError],
        ["1e-05", TypeConversionError],
        [inf, TypeConversionError],
        ["あ", TypeConversionError],
        ["漢字".encode("utf_8"), TypeConversionError],
    ])
    def test_exception(self, value, expected):
        converter = dpcc.IntegerConverter(value)

        with pytest.raises(expected):
            converter.convert()

        assert converter.try_convert() is None


class Test_FloatConverter_convert:

    @pytest.mark.parametrize(["value", "expected"], [
        [0.0, 0.0],
        [0.1, Decimal('0.1')],
        [-0.1, Decimal('-0.1')],
        [1, Decimal("1")], [-1, Decimal("-1")],
        ["0.0", Decimal("0.0")], ["0.1", Decimal("0.1")],
        ["-0.1", Decimal("-0.1")],
        ["1", Decimal("1")], ["-1", Decimal("-1")],
        [.5, .5],
        [0., 0.0],
        ["1e-05", Decimal('0.00001')],
        [inf, inf],
        [True, Decimal("1")],
    ])
    def test_normal(self, value, expected):
        converter = dpcc.FloatConverter(value)
        typeobj = FloatType(value)

        assert converter.convert() == expected
        assert converter.try_convert() == expected
        assert typeobj.convert() == expected
        assert typeobj.try_convert() == expected

    @pytest.mark.parametrize(["value", "expected"], [
        ["", TypeConversionError],
        [None, TypeConversionError],
        ["test", TypeConversionError],
        ["あ", TypeConversionError],
        ["漢字".encode("utf_8"), TypeConversionError],
    ])
    def test_exception(self, value, expected):
        converter = dpcc.FloatConverter(value)
        typeobj = FloatType(value)

        with pytest.raises(expected):
            converter.convert()

        assert converter.try_convert() is None

        with pytest.raises(expected):
            assert typeobj.convert() == expected

        assert typeobj.try_convert() is None


class Test_BoolConverter_convert:

    @pytest.mark.parametrize(["value", "expected"], [
        [True, True],
        [False, False],
        ["True", True],
        ["False", False],
        ["true", True],
        ["false", False],
    ])
    def test_normal(self, value, expected):
        converter = dpcc.BoolConverter(value)
        typeobj = BoolType(value)

        assert converter.convert() == expected
        assert converter.try_convert() == expected
        assert typeobj.convert() == expected
        assert typeobj.try_convert() == expected

    @pytest.mark.parametrize(["value", "expected"], [
        ["", TypeConversionError],
        ["t", TypeConversionError],
        ["f", TypeConversionError],
        ["yes", TypeConversionError],
        ["no", TypeConversionError],
        [0, TypeConversionError],
        [1, TypeConversionError],
        [None, TypeConversionError],
        [inf, TypeConversionError],
        [nan, TypeConversionError],
        ["あ", TypeConversionError],
        ["漢字".encode("utf_8"), TypeConversionError],
    ])
    def test_exception(self, value, expected):
        converter = dpcc.BoolConverter(value)
        typeobj = BoolType(value)

        with pytest.raises(expected):
            converter.convert()

        assert converter.try_convert() is None

        with pytest.raises(expected):
            assert typeobj.convert() == expected

        assert typeobj.try_convert() is None


class Test_DateTimeConverter_convert:

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
        converter = dpcc.DateTimeConverter(value)
        typeobj = DateTimeType(value)

        assert converter.convert() == expected
        assert converter.try_convert() == expected
        assert typeobj.convert() == expected
        assert typeobj.try_convert() == expected

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
        dt_converter = dpcc.DateTimeConverter(value)
        typeobj = DateTimeType(value)

        assert str(dt_converter) == expected
        assert str(dt_converter.convert()) == expected

    @pytest.mark.parametrize(["value", "expected"], [
        ["invalid time string", TypeConversionError],
        [None, TypeConversionError],
        [11111, TypeConversionError],
        ["あ", TypeConversionError],
        ["漢字".encode("utf_8"), TypeConversionError],
    ])
    def test_exception(self, value, expected):
        converter = dpcc.DateTimeConverter(value)
        typeobj = DateTimeType(value)

        with pytest.raises(expected):
            converter.convert()

        assert converter.try_convert() is None

        with pytest.raises(expected):
            assert typeobj.convert() == expected

        assert typeobj.try_convert() is None
