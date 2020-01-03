# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

from __future__ import unicode_literals

import pytest
import six
from six import text_type
from typepy import Nan

from dataproperty import MinMaxContainer


@pytest.fixture
def container():
    return MinMaxContainer()


class Test_MinMaxContainer_property(object):
    def test_null(self, container):
        assert container.min_value is None
        assert container.max_value is None


class Test_MinMaxContainer_repr(object):
    @pytest.mark.parametrize(
        ["values", "expected"],
        [[[1, 3], "min=1, max=3"], [[1], "min=1, max=1"], [[None, None], "None"]],
    )
    def test_normal(self, values, expected):
        assert text_type(MinMaxContainer(values)) == expected


class Test_MinMaxContainer_eq_ne(object):
    @pytest.mark.parametrize(
        ["lhs", "rhs", "expected"],
        [
            [MinMaxContainer([1, 3]), MinMaxContainer([1, 3]), True],
            [MinMaxContainer([1, 3]), MinMaxContainer([1, 4]), False],
            [MinMaxContainer([1, 3]), MinMaxContainer([0, 3]), False],
            [MinMaxContainer([1, 3]), MinMaxContainer([0, 4]), False],
        ],
    )
    def test_normal(self, lhs, rhs, expected):
        assert (lhs == rhs) == expected
        assert (lhs != rhs) == (not expected)


class Test_MinMaxContainer_contains(object):
    @pytest.mark.parametrize(
        ["lhs", "rhs", "expected"],
        [
            [1, MinMaxContainer([1, 3]), True],
            [3, MinMaxContainer([1, 3]), True],
            [0, MinMaxContainer([1, 3]), False],
            [4, MinMaxContainer([1, 3]), False],
        ],
    )
    def test_normal(self, lhs, rhs, expected):
        assert (lhs in rhs) == expected


class Test_MinMaxContainer_mean(object):
    def test_normal(self, container):
        for value in [1, 3]:
            container.update(value)

        assert container.has_value()
        assert not container.is_zero()
        assert container.mean() == 2

    def test_null(self, container):
        assert Nan(container.mean()).is_type()


class Test_MinMaxContainer_diff(object):
    def test_normal(self, container):
        for value in [1, 3]:
            container.update(value)

        assert container.has_value()
        assert not container.is_zero()
        assert container.diff() == 2

    def test_null(self, container):
        assert Nan(container.diff()).is_type()


class Test_MinMaxContainer_update(object):
    def test_normal_0(self, container):
        for value in [1, 2, 3]:
            container.update(value)

        assert container.has_value()
        assert not container.is_zero()
        assert container.min_value == 1
        assert container.max_value == 3

    def test_normal_1(self, container):
        for value in [None, -six.MAXSIZE, 0, None, six.MAXSIZE, None]:
            container.update(value)

        assert container.has_value()
        assert not container.is_zero()
        assert container.min_value == -six.MAXSIZE
        assert container.max_value == six.MAXSIZE


class Test_MinMaxContainer_merge(object):
    def test_normal(self, container):
        for value in [1, 2, 3]:
            container.update(value)

        other = MinMaxContainer([0, 10])

        container.merge(other)

        assert container.has_value()
        assert not container.is_zero()
        assert container.min_value == 0
        assert container.max_value == 10


class Test_MinMaxContainer_is_zero(object):
    @pytest.mark.parametrize(
        ["values", "expected"],
        [
            [[0, 0], True],
            [[0, 0, 0], True],
            [[0, 1], False],
            [[1, 0], False],
            [[1, 1, 1], False],
            [[None, None], False],
        ],
    )
    def test_normal(self, container, values, expected):
        assert MinMaxContainer(values).is_zero() == expected


class Test_MinMaxContainer_is_same_value(object):
    @pytest.mark.parametrize(
        ["values", "expected"],
        [
            [[0, 0], True],
            [[0, 0, 0], True],
            [[1, 1, 1], True],
            [[0, 1], False],
            [[1, 0], False],
            [[None, None], False],
        ],
    )
    def test_normal(self, container, values, expected):
        assert MinMaxContainer(values).is_same_value() == expected
