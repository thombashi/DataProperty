# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <gogogo.vm@gmail.com>
"""

from __future__ import unicode_literals

import pytest
import six

from dataproperty import *


@pytest.fixture
def container():
    return MinMaxContainer()


class Test_MinMaxContainer_property:

    def test_null(self, container):
        assert container.min_value is None
        assert container.max_value is None


class Test_MinMaxContainer_repr:

    def test_normal(self):
        container = MinMaxContainer([1, 3])
        assert str(container) == "min=1, max=3"

    def test_null(self, container):
        assert container.min_value is None
        assert container.max_value is None


class Test_MinMaxContainer_eq_ne:

    @pytest.mark.parametrize(["lhs", "rhs", "expected"], [
        [
            MinMaxContainer([1, 3]),
            MinMaxContainer([1, 3]),
            True,
        ],
        [
            MinMaxContainer([1, 3]),
            MinMaxContainer([1, 4]),
            False,
        ],
        [
            MinMaxContainer([1, 3]),
            MinMaxContainer([0, 3]),
            False,
        ],
        [
            MinMaxContainer([1, 3]),
            MinMaxContainer([0, 4]),
            False,
        ],
    ])
    def test_normal(self, lhs, rhs, expected):
        assert (lhs == rhs) == expected
        assert (lhs != rhs) == (not expected)


class Test_MinMaxContainer_contains:

    @pytest.mark.parametrize(["lhs", "rhs", "expected"], [
        [
            1,
            MinMaxContainer([1, 3]),
            True,
        ],
        [
            3,
            MinMaxContainer([1, 3]),
            True,
        ],
        [
            0,
            MinMaxContainer([1, 3]),
            False,
        ],
        [
            4,
            MinMaxContainer([1, 3]),
            False,
        ],
    ])
    def test_normal(self, lhs, rhs, expected):
        assert (lhs in rhs) == expected


class Test_MinMaxContainer_mean:

    def test_normal(self, container):
        for value in [1, 3]:
            container.update(value)

        assert container.mean() == 2

    def test_null(self, container):
        assert NanType(container.mean()).is_type()


class Test_MinMaxContainer_diff:

    def test_normal(self, container):
        for value in [1, 3]:
            container.update(value)

        assert container.diff() == 2

    def test_null(self, container):
        assert NanType(container.diff()).is_type()


class Test_MinMaxContainer_update:

    def test_normal_0(self, container):
        for value in [1, 2, 3]:
            container.update(value)

        assert container.min_value == 1
        assert container.max_value == 3

    def test_normal_1(self, container):
        for value in [None, -six.MAXSIZE, 0, None, six.MAXSIZE, None]:
            container.update(value)

        assert container.min_value == -six.MAXSIZE
        assert container.max_value == six.MAXSIZE
