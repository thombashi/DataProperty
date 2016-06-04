# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <gogogo.vm@gmail.com>
"""

from __future__ import absolute_import

import pytest

from dataproperty import IntegerTypeCheckerCreator
from dataproperty import FloatTypeCheckerCreator
from dataproperty import DateTimeTypeCheckerCreator
from dataproperty import IntegerTypeChecker
from dataproperty import FloatTypeChecker
from dataproperty import DateTimeTypeChecker


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
