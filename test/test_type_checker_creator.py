# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <gogogo.vm@gmail.com>
"""

from __future__ import absolute_import

import pytest

from dataproperty._type_checker_creator import IntegerTypeCheckerCreator
from dataproperty._type_checker_creator import FloatTypeCheckerCreator
from dataproperty._type_checker_creator import DateTimeTypeCheckerCreator
from dataproperty._type_checker import IntegerTypeChecker
from dataproperty._type_checker import FloatTypeChecker
from dataproperty._type_checker import DateTimeTypeChecker


class Test_TypeCheckerCreator(object):

    @pytest.mark.parametrize(["value", "is_convert", "expected"], [
        [IntegerTypeCheckerCreator, True, IntegerTypeChecker],
        [IntegerTypeCheckerCreator, False, IntegerTypeChecker],
        [FloatTypeCheckerCreator, True, FloatTypeChecker],
        [FloatTypeCheckerCreator, False, FloatTypeChecker],
        [DateTimeTypeCheckerCreator, True, DateTimeTypeChecker],
        [DateTimeTypeCheckerCreator, False, DateTimeTypeChecker],
    ])
    def test_normal(self, value, is_convert, expected):
        creator = value()
        type_checker = creator.create(None, is_convert)
        assert isinstance(type_checker, expected)
