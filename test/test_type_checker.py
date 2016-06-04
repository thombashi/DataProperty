# encoding: utf-8


"""
.. codeauthor:: Tsuyoshi Hombashi <gogogo.vm@gmail.com>
"""

import datetime

import pytest

from dataproperty import IntegerTypeChecker
from dataproperty import FloatTypeChecker


nan = float("nan")
inf = float("inf")


class Test_IntegerTypeChecker:

    @pytest.mark.parametrize(["value", "is_convert"], [
        [0, True], [0, False],
        [99999999999, True], [99999999999, False],
        [-99999999999, True], [-99999999999, False],
        [1234567890123456789, True], [-1234567890123456789, False],
        ["0", True],
        ["99999999999", True],
        ["-99999999999", True],
        [" 1 ", True],
    ])
    def test_normal_true(self, value, is_convert):
        assert IntegerTypeChecker(value, is_convert).is_type()

    @pytest.mark.parametrize(["value", "is_convert"], [
        ["", True], ["", False],
        [None, True], [None, False],
        [nan, True], [nan, False],
        [inf, True], [inf, False],
        [0.5, True], [0.5, False],
        ["0.5", True], ["0.5", False],
        [.999, True], [.999, False],
        [".999", True], [".999", False],
        ["test", True], ["test", False],
        ["1a1", True], ["1a1", False],
        ["11a", True], ["11a", False],
        ["a11", True], ["a11", False],
        [True, True], [True, False],
        [1e-05, True], [1e-05, False],
        [-1e-05, True], [-1e-05, False],
        ["1e-05", True], ["1e-05", False],
        ["-1e-05", True], ["-1e-05", False],
        [-0.00001, True], [-0.00001, False],
        ["0", False],
        ["0xff", True], ["0xff", False],

        ["99999999999", False],
        ["-99999999999", False],
        [" 1 ", False],
    ])
    def test_normal_false(self, value, is_convert):
        assert not IntegerTypeChecker(value, is_convert).is_type()


class Test_FloatTypeChecker:

    @pytest.mark.parametrize(["value", "is_convert"], [
        [0.0, True], [0.0, False],
        [0.1, True], [0.1, False],
        [-0.1, True], [-0.1, False],
        [1, True],
        [-1, True],
        ["0.0", True],
        ["0.1", True],
        ["-0.1", True],
        ["1", True],
        ["-1", True],
        [.5, True], [.5, False],
        [0., True], [0., False],
        ["1e-05", True],
        [nan, True], [nan, False],
        [inf, True], [inf, False],
    ])
    def test_normal_true(self, value, is_convert):
        assert FloatTypeChecker(value, is_convert).is_type()

    @pytest.mark.parametrize(["value", "is_convert"], [
        [1, False],
        [-1, False],
        ["0.1", False],
        ["0.0", False],
        ["-0.1", False],
        ["-1", False],
        ["1", False],
        ["1e-05", False],
        ["", True], ["", False],
        [None, True], [None, False],
        ["test", True], ["test", False],
        ["inf", True], ["inf", False],
        [True, True], [True, False],
    ])
    def test_normal_false(self, value, is_convert):
        assert not FloatTypeChecker(value, is_convert).is_type()
