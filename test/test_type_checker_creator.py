# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <gogogo.vm@gmail.com>
"""

from __future__ import absolute_import

import pytest

import dataproperty.type as tc


class Test_TypeCheckerCreator(object):

    @pytest.mark.parametrize(["value", "is_convert", "expected"], [
        [tc.NoneTypeCheckerCreator, True, tc.NoneTypeChecker],
        [tc.NoneTypeCheckerCreator, False, tc.NoneTypeChecker],
        [tc.IntegerTypeCheckerCreator, True, tc.IntegerTypeChecker],
        [tc.IntegerTypeCheckerCreator, False, tc.IntegerTypeChecker],
        [tc.FloatTypeCheckerCreator, True, tc.FloatTypeChecker],
        [tc.FloatTypeCheckerCreator, False, tc.FloatTypeChecker],
        [tc.DateTimeTypeCheckerCreator, True, tc.DateTimeTypeChecker],
        [tc.DateTimeTypeCheckerCreator, False, tc.DateTimeTypeChecker],
    ])
    def test_normal(self, value, is_convert, expected):
        creator = value()
        type_checker = creator.create(None, is_convert)
        assert isinstance(type_checker, expected)
