# encoding: utf-8


"""
.. codeauthor:: Tsuyoshi Hombashi <gogogo.vm@gmail.com>
"""

from __future__ import unicode_literals

import datetime
import itertools

from dateutil.tz import tzoffset
import pytest
import six

from dataproperty._type_checker import *
from dataproperty import *
from decimal import Decimal


nan = float("nan")
inf = float("inf")


class Test_NoneTypeChecker_is_type:

    @pytest.mark.parametrize(["value", "is_convert", "expected"], [
        [None, True, True],
        [None, False, True],
    ] + list(
        itertools.product(
            [
                "None",
                True, False, 0, six.MAXSIZE, inf, nan,
            ],
            [True, False],
            [False]
        ))
    )
    def test_normal_true(self, value, is_convert, expected):
        is_strict = not is_convert
        expected_typecode = Typecode.NONE

        type_checker = NoneTypeChecker(value, is_strict)
        typeobj = NoneType(value, is_strict)

        assert type_checker.is_type() == expected
        assert type_checker.typecode == expected_typecode
        assert typeobj.is_type() == expected
        assert typeobj.typecode == expected_typecode


class Test_NoneTypeChecker_validate:

    @pytest.mark.parametrize(["value", "is_convert"], [
        [None, True],
        [None, False],
    ])
    def test_normal(self, value, is_convert):
        is_strict = not is_convert

        type_checker = NoneTypeChecker(value, is_strict)
        type_checker.validate()

    @pytest.mark.parametrize(
        ["value", "is_convert", "expected"],
        list(itertools.product(
            [
                "None",
                True, False, 0, six.MAXSIZE, inf, nan,
            ],
            [True, False],
            [TypeError]
        ))
    )
    def test_exception(self, value, is_convert, expected):
        is_strict = not is_convert

        type_checker = NoneTypeChecker(value, is_strict)
        with pytest.raises(expected):
            type_checker.validate()


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
            ["None", "いろは", "いろは".encode("utf_8")],
            [True, False],
            [True]
        ))
    )
    def test_normal_true(self, value, is_convert, expected):
        is_strict = not is_convert

        type_checker = StringTypeChecker(value, is_strict)
        assert type_checker.is_type() == expected
        assert type_checker.typecode == Typecode.STRING


class Test_StringTypeChecker_validate:

    @pytest.mark.parametrize(["value", "is_convert"],  [
        [None, True],
        [six.MAXSIZE, True],
        [inf, True],
        ["", False],
    ] + list(
        itertools.product(
            ["None", ],
            [True, False],
        ))
    )
    def test_normal(self, value, is_convert):
        is_strict = not is_convert

        type_checker = StringTypeChecker(value, is_strict)
        type_checker.validate()

    @pytest.mark.parametrize(["value", "is_convert", "expected"], [
        [None, False, TypeError],
        [six.MAXSIZE, False, TypeError],
        [inf, False, TypeError],
        [nan, False, TypeError],
    ])
    def test_exception(self, value, is_convert, expected):
        is_strict = not is_convert

        type_checker = StringTypeChecker(value, is_strict)
        with pytest.raises(expected):
            type_checker.validate()


class Test_IntegerTypeChecker_is_type:

    @pytest.mark.parametrize(["value", "is_convert"], [
        ["0", True],
        [" 1 ", True],
        [str(six.MAXSIZE), True], [str(-six.MAXSIZE), True],
    ] + list(
        itertools.product(
            [0, six.MAXSIZE, -six.MAXSIZE, Decimal("1")],
            [True, False],
        ))
    )
    def test_normal_true(self, value, is_convert):
        is_strict = not is_convert

        type_checker = IntegerTypeChecker(value, is_strict)
        assert type_checker.is_type()
        assert type_checker.typecode == Typecode.INTEGER

    @pytest.mark.parametrize(["value", "is_convert"], [
        ["0", False],
        ["0xff", True], ["0xff", False],
        [" 1 ", False],
        [str(six.MAXSIZE), False], [str(-six.MAXSIZE), False],
    ] + list(
        itertools.product(
            [
                None, True,
                nan, inf, 0.5, "0.5", .999, ".999", Decimal("1.1"),
                "", "test", "1a1", "11a", "a11",
                1e-05, -1e-05, "1e-05", "-1e-05",

            ],
            [True, False],
        ))
    )
    def test_normal_false(self, value, is_convert):
        is_strict = not is_convert

        assert not IntegerTypeChecker(value, is_strict).is_type()


class Test_IntegerTypeChecker_validate:

    @pytest.mark.parametrize(["value", "is_convert"],  [
        ["0", True],
        [" 1 ", True],
        [str(six.MAXSIZE), True], [str(-six.MAXSIZE), True],
    ] + list(
        itertools.product(
            [0, six.MAXSIZE, -six.MAXSIZE],
            [True, False],
        ))
    )
    def test_normal(self, value, is_convert):
        is_strict = not is_convert

        type_checker = IntegerTypeChecker(value, is_strict)
        type_checker.validate()

    @pytest.mark.parametrize(["value", "is_convert"], [
        ["0", False],
        ["0xff", True], ["0xff", False],
        [" 1 ", False],
        [str(six.MAXSIZE), False], [str(-six.MAXSIZE), False],
    ] + list(
        itertools.product(
            [
                None, True,
                nan, inf, 0.5, "0.5", .999, ".999", Decimal("1.1"),
                "", "test", "1a1", "11a", "a11",
                1e-05, -1e-05, "1e-05", "-1e-05",
            ],
            [True, False],
        ))
    )
    def test_exception(self, value, is_convert):
        is_strict = not is_convert

        type_checker = IntegerTypeChecker(value, is_strict)
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
        is_strict = not is_convert

        type_checker = FloatTypeChecker(value, is_strict)
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
            [
                "", None, "test", True,
            ],
            [True, False],
        ))
    )
    def test_normal_false(self, value, is_convert):
        is_strict = not is_convert

        assert not FloatTypeChecker(value, is_strict).is_type()


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
        is_strict = not is_convert

        type_checker = BoolTypeChecker(value, is_strict)
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
        is_strict = not is_convert

        type_checker = BoolTypeChecker(value, is_strict)
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
        [
            "100-0004",
            True,
        ],
    ])
    def test_normal_true(self, value, is_convert):
        is_strict = not is_convert

        type_checker = DateTimeTypeChecker(value, is_strict)
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
        is_strict = not is_convert

        assert not DateTimeTypeChecker(value, is_strict).is_type()


class Test_InfinityChecker_is_type:

    @pytest.mark.parametrize(
        ["value", "is_convert", "expected"],
        list(itertools.product(
            [
                0.0, six.MAXSIZE, "0", nan,

            ],
            [True, False],
            [False]
        )) + list(itertools.product(
            [inf],
            [True, False],
            [True]
        )) + [
            ["inf", True, True],
            ["inf", False, False],
            ["-infinity", True, True],
            ["-infinity", False, False],
            ["INF", True, True],
            ["INF", False, False],
        ]
    )
    def test_normal(self, value, is_convert, expected):
        is_strict = not is_convert

        type_checker = InfinityChecker(value, is_strict)
        assert type_checker.is_type() == expected
        assert type_checker.typecode == Typecode.INFINITY


class Test_NanChecker_is_type:

    @pytest.mark.parametrize(
        ["value", "is_convert", "expected"],
        list(itertools.product(
            [
                0.0, six.MAXSIZE, "0", inf,

            ],
            [True, False],
            [False]
        )) + list(itertools.product(
            [nan, Decimal("NaN")],
            [True, False],
            [True]
        )) + [
            ["nan", True, True],
            ["nan", False, False],
            ["-Nan", True, True],
            ["-Nan", False, False],
            ["NAN", True, True],
            ["NAN", False, False],
        ]
    )
    def test_normal(self, value, is_convert, expected):
        is_strict = not is_convert

        type_checker = NanChecker(value, is_strict)
        assert type_checker.is_type() == expected
        assert type_checker.typecode == Typecode.NAN


class Test_DictionaryTypeChecker_is_type:

    @pytest.mark.parametrize(["value", "is_strict"], [
        [[["a", 1]], False],
        [(("a", 1), ), False]
    ] + list(
        itertools.product(
            [{}],
            [True, False],
        ))
    )
    def test_normal_true(self, value, is_strict):
        type_checker = DictionaryTypeChecker(value, is_strict)
        assert type_checker.is_type()
        assert type_checker.typecode == Typecode.DICTIONARY

    @pytest.mark.parametrize(["value", "is_strict"], [
        [[["a", 1]], True],
        [(("a", 1), ), True]
    ] + list(
        itertools.product(
            [1, "a", nan, True, ],
            [True, False],
        ))
    )
    def test_normal_false(self, value, is_strict):
        type_checker = DictionaryTypeChecker(value, is_strict)
        assert not type_checker.is_type()
