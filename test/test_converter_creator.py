# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <gogogo.vm@gmail.com>
"""

from __future__ import absolute_import

import pytest

import dataproperty.converter as dpc
import dataproperty.converter._core as dpcc


class Test_ConverterCreator(object):

    @pytest.mark.parametrize(["value", "expected"], [
        [dpc.NopConverterCreator, dpcc.NopConverter],
        [dpc.StringConverterCreator, dpcc.StringConverter],
        [dpc.IntegerConverterCreator, dpcc.IntegerConverter],
        [dpc.FloatConverterCreator, dpcc.FloatConverter],
        [dpc.BoolConverterCreator, dpcc.BoolConverter],
        [dpc.DateTimeConverterCreator, dpcc.DateTimeConverter],
    ])
    def test_normal(self, value, expected):
        creator = value()
        type_checker = creator.create(None)
        assert isinstance(type_checker, expected)
