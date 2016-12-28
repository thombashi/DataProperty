# encoding: utf-8


"""
.. codeauthor:: Tsuyoshi Hombashi <gogogo.vm@gmail.com>
"""

from __future__ import unicode_literals

import pytest
import six
from six.moves import range

from dataproperty import *


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

        # float not enough precision
        [10000000000000000000.99, 20], [-10000000000000000000.99, 20],

        ["10000000000000000000", 20], ["-10000000000000000000", 20],
        ["99999999999999099999.99", 20], ["-99999999999999099999.99", 20],
    ])
    def test_normal(self, value, expected):
        assert get_integer_digit(value) == expected

    @pytest.mark.parametrize(["value", "expected"], [
        [999999999999999999999999999999.9999999999, 31],
        [-999999999999999999999999999999.9999999999, 31],
        ["999999999999999999999999999999.9999999999", 30],
        ["-999999999999999999999999999999.9999999999", 30],
    ])
    def test_abnormal(self, value, expected):
        assert get_integer_digit(value) == expected

    @pytest.mark.parametrize(["value", 'exception'], [
        [True, TypeError],
        [False, TypeError],
        [None, TypeError],
        ["test", TypeError],
        ["a", TypeError],
        ["0xff", TypeError],
        [nan, ValueError],
        [inf, ValueError],
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
        ["0xff"], ["test"], ["いろは".encode("utf_8")]
    ])
    def test_nan(self, value):
        integer_digits, decimal_places = get_number_of_digit(value)
        assert NanType(integer_digits).is_type()
        assert NanType(decimal_places).is_type()
