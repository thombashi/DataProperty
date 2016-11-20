# encoding: utf-8


"""
.. codeauthor:: Tsuyoshi Hombashi <gogogo.vm@gmail.com>
"""

import datetime
from decimal import Decimal

from dataproperty import *
import pytest
import six
from six.moves import range


nan = float("nan")
inf = float("inf")


class Test_is_hex:

    @pytest.mark.parametrize(["value"], [
        ["0x00"], ["0xffffffff"], ["a"], ["f"],
    ])
    def test_normal(self, value):
        assert is_hex(value)

    @pytest.mark.parametrize(["value"], [
        [None], [nan], [inf],
        [0], [1], [0.5],
        ["test"], ["g"],
        [True],
    ])
    def test_abnormal(self, value):
        assert not is_hex(value)


class Test_is_not_empty_string:

    @pytest.mark.parametrize(["value", "expected"], [
        ["nan", True],
        ["テスト", True],

        [None, False],
        ["", False],
        ["  ", False],
        ["\t", False],
        ["\n", False],
        [[], False],
        [1, False],
        [True, False],
        [nan, False],
        [Decimal("nan"), False],
    ])
    def test_normal(self, value, expected):
        assert is_not_empty_string(value) == expected


class Test_is_empty_string:

    @pytest.mark.parametrize(["value", "expected"], [
        ["nan", False],
        ["テスト", False],

        [None, True],
        ["", True],
        ["  ", True],
        ["\t", True],
        ["\n", True],
        [True, True],
        [[], True],
        [1, True],
    ])
    def test_normal(self, value, expected):
        assert is_empty_string(value) == expected


class Test_is_list_or_tuple:

    @pytest.mark.parametrize(["value", "expected"], [
        [[], True],
        [[1], True],
        [["a"] * 200000, True],
        [(), True],
        [(1,), True],
        [("a",) * 200000, True],

        [None, False],
        [nan, False],
        [0, False],
        ["aaa", False],
        [True, False],
    ])
    def test_normal(self, value, expected):
        assert is_list_or_tuple(value) == expected


class Test_is_empty_sequence:

    @pytest.mark.parametrize(["value", "expected"], [
        [(), True],
        [[], True],
        ["", True],
        [range(0), True],

        [[1], False],
        [["a"] * 200000, False],
        [(1,), False],
        [("a",) * 200000, False],
        ["aaa", False],
        [range(0, 10), False],

        [True, False],
        [False, False],
        [six.MAXSIZE, False],
        [0.1, False],
        [nan, False],
        [inf, False],
    ])
    def test_normal(self, value, expected):
        assert is_empty_sequence(value) == expected


class Test_is_not_empty_sequence:

    @pytest.mark.parametrize(["value", "expected"], [
        [[1], True],
        [["a"] * 200000, True],
        [(1,), True],
        [("a",) * 200000, True],
        ["a" * 200000, True],
        [range(0, 10), True],

        [(), False],
        [[], False],
        [None, False],
        [range(0), False],

        [True, False],
        [False, False],
        [six.MAXSIZE, False],
        [0.1, False],
        [nan, False],
        [inf, False],
    ])
    def test_normal(self, value, expected):
        assert is_not_empty_sequence(value) == expected


class Test_get_integer_digit:

    @pytest.mark.parametrize(["value", "expected"], [
        [0, 1], [-0, 1],
        [.99, 1], [-.99, 1],
        [".99", 1], ["-.99", 1],
        [1.01, 1], [-1.01, 1],
        [9.99, 1], [-9.99, 1],
        ["9.99", 1], ["-9.99", 1],
        ["0", 1], ["-0", 1],

        [10, 2], [-10, 2],
        [99.99, 2], [-99.99, 2],
        ["10", 2], ["-10", 2],
        ["99.99", 2], ["-99.99", 2],

        [100, 3], [-100, 3],
        [999.99, 3], [-999.99, 3],
        ["100", 3], ["-100", 3],
        ["999.99", 3], ["-999.99", 3],

        [10000000000000000000, 20], [-10000000000000000000, 20],
        [99999999999999099999.99, 20], [-99999999999999099999.99, 20],
        ["10000000000000000000", 20], ["-10000000000000000000", 20],
        ["99999999999999099999.99", 20], ["-99999999999999099999.99", 20],
    ])
    def test_normal(self, value, expected):
        assert get_integer_digit(value) == expected

    @pytest.mark.parametrize(["value", "expected"], [
        [99999999999999999999.99, 21],
        [-99999999999999999999.99, 21],
        ["99999999999999999999.99", 21],
        ["-99999999999999999999.99", 21],
    ])
    def test_abnormal(self, value, expected):
        # expected result == 20
        assert get_integer_digit(value) == expected

    @pytest.mark.parametrize(["value", 'exception'], [
        [True, TypeError],
        [False, TypeError],
        [None, TypeError],
        ["test", ValueError],
        ["a", ValueError],
        ["0xff", ValueError],
        [nan, ValueError],
        [inf, OverflowError],
    ])
    def test_exception(self, value, exception):
        with pytest.raises(exception):
            get_integer_digit(value)


class Test_get_number_of_digit:

    @pytest.mark.parametrize(["value", "expected"], [
        [0, (1, 0)], [-0, (1, 0)],
        ["0", (1, 0)], ["-0", (1, 0)],
        [10, (2, 0)], [-10, (2, 0)],
        ["10", (2, 0)], ["-10", (2, 0)],
        [10.1, (2, 1)], [-10.1, (2, 1)],
        ["10.1", (2, 1)], ["-10.1", (2, 1)],
        [10.01, (2, 2)], [-10.01, (2, 2)],
        [10.001, (2, 2)], [-10.001, (2, 2)],
        [100.1, (3, 1)], [-100.1, (3, 1)],
        [100.01, (3, 1)], [-100.01, (3, 1)],
        [0.1, (1, 1)], [-0.1, (1, 1)],
        ["0.1", (1, 1)], ["-0.1", (1, 1)],
        [.99, (1, 2)], [-.99, (1, 2)],
        [".99", (1, 2)], ["-.99", (1, 2)],
        [0.01, (1, 2)], [-0.01, (1, 2)],
        ["0.01", (1, 2)], ["-0.01", (1, 2)],
        [0.001, (1, 3)], [-0.001, (1, 3)],
        ["0.001", (1, 3)], ["-0.001", (1, 3)],
        [0.0001, (1, 4)], [-0.0001, (1, 4)],
        ["0.0001", (1, 4)], ["-0.0001", (1, 4)],
        [0.00001, (1, 4)], [-0.00001, (1, 4)],
        ["0.00001", (1, 4)], ["-0.00001", (1, 4)],
        [2e-05, (1, 4)], [-2e-05, (1, 4)],
        ["2e-05", (1, 4)], ["-2e-05", (1, 4)],
    ])
    def test_normal(self, value, expected):
        assert get_number_of_digit(value) == expected

    @pytest.mark.parametrize(["value"], [
        [None],
        [True],
        [inf],
        [nan],
        ["0xff"], ["test"],
    ])
    def test_nan(self, value):
        integer_digits, decimal_places = get_number_of_digit(value)
        assert NanType(integer_digits).is_type()
        assert NanType(decimal_places).is_type()


class Test_to_unicode:

    @pytest.mark.parametrize(["value", "expected"], [
        [u"吾輩は猫である", u"吾輩は猫である"],
        ["吾輩は猫である", u"吾輩は猫である"],
        ["マルチバイト文字", u"マルチバイト文字"],
        ["abcdef", u"abcdef"],
        [None, u"None"],
        ["", u""],
        [True, u"True"],
        [[], u"[]"],
        [1, u"1"],
    ])
    def test_normal(self, value, expected):
        unicode_str = to_unicode(value)

        assert unicode_str == expected
        assert to_unicode(unicode_str) == unicode_str


class Test_is_multibyte_str:

    @pytest.mark.parametrize(["value", "expected"], [
        [u"吾輩は猫である", True],
        ["吾輩は猫である", True],
        ["abcdef", False],
        [None, False],
        ["", False],
        [True, False],
        [[], False],
        [1, False],
    ])
    def test_normal(self, value, expected):
        assert is_multibyte_str(value) == expected


class Test_get_ascii_char_width:

    @pytest.mark.parametrize(["value", "expected"], [
        [u"吾輩は猫である", 14],
        [u"いaろbはc", 9],
        [u"abcdef", 6],
        [u"", 0],
    ])
    def test_normal(self, value, expected):
        assert get_ascii_char_width(value) == expected

    @pytest.mark.parametrize(["value", "expected"], [
        [six.b("abcdef"), TypeError],
        [None, TypeError],
        [True, TypeError],
        [1, TypeError],
        [nan, TypeError],
    ])
    def test_exception(self, value, expected):
        with pytest.raises(expected):
            get_ascii_char_width(value)
