# encoding: utf-8


"""
.. codeauthor:: Tsuyoshi Hombashi <gogogo.vm@gmail.com>
"""

import datetime
import itertools

from dateutil.tz import tzoffset
import pytest
import six

import dataproperty.type as tc
from dataproperty import Typecode
from decimal import Decimal


nan = float("nan")
inf = float("inf")


class Test_NoneTypeChecker_is_type:

    @pytest.mark.parametrize(["value", "is_convert", "expected"], [
        [None, True, True],
        [None, False, True],
    ] + list(
        itertools.product(
            ["None", True, False, 0, six.MAXSIZE, inf, nan],
            [True, False],
            [False]
        ))
    )
    def test_normal_true(self, value, is_convert, expected):
        type_checker = tc.NoneTypeChecker(value, is_convert)
        assert type_checker.is_type() == expected
        assert type_checker.typecode == Typecode.NONE


class Test_NoneTypeChecker_validate:

    @pytest.mark.parametrize(["value", "is_convert"], [
        [None, True],
        [None, False],
    ])
    def test_normal(self, value, is_convert):
        type_checker = tc.NoneTypeChecker(value, is_convert)
        type_checker.validate()

    @pytest.mark.parametrize(
        ["value", "is_convert", "exception_type", "expected"],
        list(itertools.product(
            ["None", True, False, 0, six.MAXSIZE, inf, nan],
            [True, False],
            [ValueError],
            [ValueError]
        )) + list(itertools.product(
            ["None", True, False, 0, six.MAXSIZE, inf, nan],
            [True, False],
            [TypeError],
            [TypeError]
        ))
    )
    def test_exception(self, value, is_convert, exception_type, expected):
        type_checker = tc.NoneTypeChecker(value, is_convert)
        with pytest.raises(expected):
            type_checker.validate(exception_type=exception_type)


class Test_StringTypeChecker_is_type:

    @pytest.mark.parametrize(["value", "is_convert", "expected"], [
        [None, True, True],
        [None, False, False],
        [six.MAXSIZE, True, True],
        [six.MAXSIZE, False, False],
        [inf, True, True],
        [inf, False, False],
    ] + list(
        itertools.product(
            ["None"],
            [True, False],
            [True]
        ))
    )
    def test_normal_true(self, value, is_convert, expected):
        type_checker = tc.StringTypeChecker(value, is_convert)
        assert type_checker.is_type() == expected
        assert type_checker.typecode == Typecode.STRING


class Test_StringTypeChecker_validate:

    @pytest.mark.parametrize(["value", "is_convert"],  [
        [None, True],
        [six.MAXSIZE, True],
        [inf, True],
    ] + list(
        itertools.product(
            ["None"],
            [True, False],
        ))
    )
    def test_normal(self, value, is_convert):
        type_checker = tc.StringTypeChecker(value, is_convert)
        type_checker.validate()

    @pytest.mark.parametrize(
        ["value", "is_convert", "exception_type", "expected"],
        [
            [None, False, ValueError, ValueError],
            [six.MAXSIZE, False, TypeError, TypeError],
            [inf, False, ValueError, ValueError],
        ]
    )
    def test_exception(self, value, is_convert, exception_type, expected):
        type_checker = tc.StringTypeChecker(value, is_convert)
        with pytest.raises(expected):
            type_checker.validate(exception_type=exception_type)


class Test_IntegerTypeChecker_is_type:

    @pytest.mark.parametrize(["value", "is_convert"], [
        ["0", True],
        [" 1 ", True],
        [str(six.MAXSIZE), True], [str(-six.MAXSIZE), True],
        [Decimal("1"), True],
    ] + list(
        itertools.product(
            [0, six.MAXSIZE, -six.MAXSIZE],
            [True, False],
        ))
    )
    def test_normal_true(self, value, is_convert):
        type_checker = tc.IntegerTypeChecker(value, is_convert)
        assert type_checker.is_type()
        assert type_checker.typecode == Typecode.INT

    @pytest.mark.parametrize(["value", "is_convert"], [
        ["0", False],
        ["0xff", True], ["0xff", False],
        [" 1 ", False],
        [str(six.MAXSIZE), False], [str(-six.MAXSIZE), False],
        [Decimal("1"), False],
    ] + list(
        itertools.product(
            [
                None, True, nan, inf, 0.5, "0.5", .999, ".999",
                "", "test", "1a1", "11a", "a11",
                1e-05, -1e-05, "1e-05", "-1e-05",
            ],
            [True, False],
        ))
    )
    def test_normal_false(self, value, is_convert):
        assert not tc.IntegerTypeChecker(value, is_convert).is_type()


class Test_IntegerTypeChecker_validate:

    @pytest.mark.parametrize(["value", "is_convert"],  [
        ["0", True],
        [" 1 ", True],
        [str(six.MAXSIZE), True], [str(-six.MAXSIZE), True],
        [Decimal("1"), True],
    ] + list(
        itertools.product(
            [0, six.MAXSIZE, -six.MAXSIZE],
            [True, False],
        ))
    )
    def test_normal(self, value, is_convert):
        type_checker = tc.IntegerTypeChecker(value, is_convert)
        type_checker.validate()

    @pytest.mark.parametrize(["value", "is_convert"], [
        ["0", False],
        ["0xff", True], ["0xff", False],
        [" 1 ", False],
        [str(six.MAXSIZE), False], [str(-six.MAXSIZE), False],
        [Decimal("1"), False],
    ] + list(
        itertools.product(
            [
                None, True, nan, inf, 0.5, "0.5", .999, ".999",
                "", "test", "1a1", "11a", "a11",
                1e-05, -1e-05, "1e-05", "-1e-05",
            ],
            [True, False],
        ))
    )
    def test_exception(self, value, is_convert):
        type_checker = tc.IntegerTypeChecker(value, is_convert)
        with pytest.raises(TypeError):
            type_checker.validate()


class Test_FloatTypeChecker_is_type:

    @pytest.mark.parametrize(["value", "is_convert"], [
        [1, True],
        [-1, True],
        ["0.0", True],
        ["0.1", True], ["-0.1", True],
        ["1", True], ["-1", True],
        ["1e-05", True],
        [six.MAXSIZE, True], [-six.MAXSIZE, True],
        [str(six.MAXSIZE), True], [str(-six.MAXSIZE), True],
        ["inf", True], ["nan", True],
    ] + list(
        itertools.product(
            [0.0, 0.1, -0.1, .5, 0., nan, inf, Decimal("1.1")],
            [True, False],
        ))
    )
    def test_normal_true(self, value, is_convert):
        type_checker = tc.FloatTypeChecker(value, is_convert)
        assert type_checker.is_type()
        assert type_checker.typecode == Typecode.FLOAT

    @pytest.mark.parametrize(["value", "is_convert"], [
        [1, False],
        [-1, False],
        ["0.0", False],
        ["0.1", False], ["-0.1", False],
        ["1", False], ["-1", False],
        ["1e-05", False],
        [six.MAXSIZE, False], [-six.MAXSIZE, False],
        [str(six.MAXSIZE), False], [str(-six.MAXSIZE), False],
        ["inf", False], ["nan", False],
    ] + list(
        itertools.product(
            ["", None, "test", True],
            [True, False],
        ))
    )
    def test_normal_false(self, value, is_convert):
        assert not tc.FloatTypeChecker(value, is_convert).is_type()


class Test_BoolTypeChecker_is_type:

    @pytest.mark.parametrize(["value", "is_convert"], [
        ["True", True],
        ["False", True],
        ["true", True],
        ["false", True],
    ] + list(
        itertools.product(
            [True, False],
            [True, False],
        ))
    )
    def test_normal_true(self, value, is_convert):
        type_checker = tc.BoolTypeChecker(value, is_convert)
        assert type_checker.is_type()
        assert type_checker.typecode == Typecode.BOOL

    @pytest.mark.parametrize(["value", "is_convert"], [
        ["True", False],
        ["False", False],
        ["true", False],
        ["false", False],
    ] + list(
        itertools.product(
            [0, 1, "yes", "no", None, inf, nan],
            [True, False],
        ))
    )
    def test_normal_false(self, value, is_convert):
        type_checker = tc.BoolTypeChecker(value, is_convert)
        assert not type_checker.is_type()


class Test_DateTimeTypeChecker_is_type:

    @pytest.mark.parametrize(["value", "is_convert"], [
        [
            datetime.datetime(
                2017, 3, 22, 10, 0, tzinfo=tzoffset(None, 32400)),
            True,
        ],
        [
            datetime.datetime(
                2017, 3, 22, 10, 0, tzinfo=tzoffset(None, 32400)),
            False,
        ],
        [
            "2017-03-22T10:00:00+0900",
            True,
        ],
    ])
    def test_normal_true(self, value, is_convert):
        type_checker = tc.DateTimeTypeChecker(value, is_convert)
        assert type_checker.is_type()
        assert type_checker.typecode == Typecode.DATETIME

    @pytest.mark.parametrize(["value", "is_convert"], [
        ["2017-03-22T10:00:00+0900", False],
        ["invalid time string", True],
        ["invalid time string", False],
        [None, True],
        [None, False],
        [six.MAXSIZE, True], [six.MAXSIZE, False],
    ])
    def test_normal_false(self, value, is_convert):
        assert not tc.DateTimeTypeChecker(value, is_convert).is_type()


class Test_InfinityChecker_is_type:

    @pytest.mark.parametrize(
        ["value", "is_convert", "expected"],
        list(itertools.product(
            [0.0, six.MAXSIZE, "0", nan],
            [True, False],
            [False]
        )) + list(itertools.product(
            [inf],
            [True, False],
            [True]
        )) + [
            ["inf", True, True],
            ["inf", False, False],
            ["INF", True, True],
            ["INF", False, False],
        ]
    )
    def test_normal(self, value, is_convert, expected):
        type_checker = tc.InfinityChecker(value, is_convert)
        assert type_checker.is_type() == expected
        assert type_checker.typecode == Typecode.INFINITY


class Test_NanChecker_is_type:

    @pytest.mark.parametrize(
        ["value", "is_convert", "expected"],
        list(itertools.product(
            [0.0, six.MAXSIZE, "0", inf],
            [True, False],
            [False]
        )) + list(itertools.product(
            [nan],
            [True, False],
            [True]
        )) + [
            ["nan", True, True],
            ["nan", False, False],
            ["NAN", True, True],
            ["NAN", False, False],
        ]
    )
    def test_normal(self, value, is_convert, expected):
        type_checker = tc.NanChecker(value, is_convert)
        assert type_checker.is_type() == expected
        assert type_checker.typecode == Typecode.NAN
