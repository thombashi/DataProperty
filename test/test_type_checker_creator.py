# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <gogogo.vm@gmail.com>
"""

from __future__ import absolute_import

import pytest

import dataproperty._type_checker_creator as tcc
import dataproperty._type_checker as tc


class Test_TypeCheckerCreator(object):

    @pytest.mark.parametrize(["value", "is_convert", "expected"], [
        [tcc.NoneTypeCheckerCreator, True, tc.NoneTypeChecker],
        [tcc.NoneTypeCheckerCreator, False, tc.NoneTypeChecker],
        [tcc.IntegerTypeCheckerCreator, True, tc.IntegerTypeChecker],
        [tcc.IntegerTypeCheckerCreator, False, tc.IntegerTypeChecker],
        [tcc.FloatTypeCheckerCreator, True, tc.FloatTypeChecker],
        [tcc.FloatTypeCheckerCreator, False, tc.FloatTypeChecker],
        [tcc.DateTimeTypeCheckerCreator, True, tc.DateTimeTypeChecker],
        [tcc.DateTimeTypeCheckerCreator, False, tc.DateTimeTypeChecker],
    ])
    def test_normal(self, value, is_convert, expected):
        creator = value()
        type_checker = creator.create(None, is_convert)
        assert isinstance(type_checker, expected)
