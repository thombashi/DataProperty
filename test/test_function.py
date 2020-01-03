# encoding: utf-8


"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

from __future__ import unicode_literals

import pytest

from dataproperty import get_integer_digit, get_number_of_digit


nan = float("nan")
inf = float("inf")


class Test_get_integer_digit(object):
    @pytest.mark.parametrize(
        ["value", "expected"],
        [
            [0, 1],
            [-0, 1],
            [0.99, 1],
            [-0.99, 1],
            [".99", 1],
            ["-.99", 1],
            [1.01, 1],
            [-1.01, 1],
            [9.99, 1],
            [-9.99, 1],
            ["9.99", 1],
            ["-9.99", 1],
            ["0", 1],
            ["-0", 1],
            [10, 2],
            [-10, 2],
            [99.99, 2],
            [-99.99, 2],
            ["10", 2],
            ["-10", 2],
            ["99.99", 2],
            ["-99.99", 2],
            [100, 3],
            [-100, 3],
            [999.99, 3],
            [-999.99, 3],
            ["100", 3],
            ["-100", 3],
            ["999.99", 3],
            ["-999.99", 3],
            [10000000000000000000, 20],
            [-10000000000000000000, 20],
            # float not enough precision
            [10000000000000000000.99, 20],
            [-10000000000000000000.99, 20],
            ["10000000000000000000", 20],
            ["-10000000000000000000", 20],
            ["99999999999999099999.99", 20],
            ["-99999999999999099999.99", 20],
        ],
    )
    def test_normal(self, value, expected):
        assert get_integer_digit(value) == expected

    @pytest.mark.parametrize(
        ["value", "expected"],
        [
            [999999999999999999999999999999.9999999999, 31],
            [-999999999999999999999999999999.9999999999, 31],
            ["999999999999999999999999999999.9999999999", 30],
            ["-999999999999999999999999999999.9999999999", 30],
        ],
    )
    def test_abnormal(self, value, expected):
        assert get_integer_digit(value) == expected

    @pytest.mark.parametrize(
        ["value", "exception"],
        [
            [True, ValueError],
            [False, ValueError],
            [None, ValueError],
            ["test", ValueError],
            ["a", ValueError],
            ["0xff", ValueError],
            [nan, ValueError],
            [inf, ValueError],
        ],
    )
    def test_exception(self, value, exception):
        with pytest.raises(exception):
            get_integer_digit(value)


class Test_get_number_of_digit(object):
    @pytest.mark.parametrize(
        ["value", "expected"],
        [
            [0, (1, 0)],
            [-0, (1, 0)],
            ["0", (1, 0)],
            ["-0", (1, 0)],
            [10, (2, 0)],
            [-10, (2, 0)],
            ["10", (2, 0)],
            ["-10", (2, 0)],
            [10.1, (2, 1)],
            [-10.1, (2, 1)],
            ["10.1", (2, 1)],
            ["-10.1", (2, 1)],
            [10.01, (2, 2)],
            [-10.01, (2, 2)],
            [10.001, (2, 2)],
            [-10.001, (2, 2)],
            [100.1, (3, 1)],
            [-100.1, (3, 1)],
            [100.01, (3, 1)],
            [-100.01, (3, 1)],
            [0.1, (1, 1)],
            [-0.1, (1, 1)],
            ["0.1", (1, 1)],
            ["-0.1", (1, 1)],
            [0.99, (1, 2)],
            [-0.99, (1, 2)],
            [".99", (1, 2)],
            ["-.99", (1, 2)],
            [0.01, (1, 2)],
            [-0.01, (1, 2)],
            ["0.01", (1, 2)],
            ["-0.01", (1, 2)],
            [0.001, (1, 3)],
            [-0.001, (1, 3)],
            ["0.001", (1, 3)],
            ["-0.001", (1, 3)],
            [0.0001, (1, 4)],
            [-0.0001, (1, 4)],
            ["0.0001", (1, 4)],
            ["-0.0001", (1, 4)],
            [0.00001, (1, 4)],
            [-0.00001, (1, 4)],
            ["0.00001", (1, 4)],
            ["-0.00001", (1, 4)],
            [2e-05, (1, 4)],
            [-2e-05, (1, 4)],
            ["2e-05", (1, 4)],
            ["-2e-05", (1, 4)],
        ],
    )
    def test_normal(self, value, expected):
        assert get_number_of_digit(value) == expected

    @pytest.mark.parametrize(
        ["value"], [[None], [True], [inf], [nan], ["0xff"], ["test"], ["いろは".encode("utf_8")]]
    )
    def test_nan(self, value):
        integer_digits, decimal_places = get_number_of_digit(value)
        assert integer_digits is None
        assert decimal_places is None
