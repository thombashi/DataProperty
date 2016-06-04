# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <gogogo.vm@gmail.com>
"""

from __future__ import absolute_import

import pytest

from dataproperty._converter import IntegerConverter
from dataproperty._converter import FloatConverter
from dataproperty._converter import DateTimeConverter
from dataproperty._converter_creator import IntegerConverterCreator
from dataproperty._converter_creator import FloatConverterCreator
from dataproperty._converter_creator import DateTimeConverterCreator


class Test_ConverterCreator(object):

    @pytest.mark.parametrize(["value", "expected"], [
        [IntegerConverterCreator, IntegerConverter],
        [FloatConverterCreator, FloatConverter],
        [DateTimeConverterCreator, DateTimeConverter],
    ])
    def test_normal(self, value, expected):
        creator = value()
        type_checker = creator.create(None)
        assert isinstance(type_checker, expected)
