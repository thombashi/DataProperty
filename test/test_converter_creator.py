# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <gogogo.vm@gmail.com>
"""

from __future__ import absolute_import

import pytest

import dataproperty.converter as dpc
from dataproperty.converter._core import NoneConverter
from dataproperty.converter._core import IntegerConverter
from dataproperty.converter._core import FloatConverter
from dataproperty.converter._core import DateTimeConverter


class Test_ConverterCreator(object):

    @pytest.mark.parametrize(["value", "expected"], [
        [dpc.NoneConverterCreator, NoneConverter],
        [dpc.IntegerConverterCreator, IntegerConverter],
        [dpc.FloatConverterCreator, FloatConverter],
        [dpc.DateTimeConverterCreator, DateTimeConverter],
    ])
    def test_normal(self, value, expected):
        creator = value()
        type_checker = creator.create(None)
        assert isinstance(type_checker, expected)
