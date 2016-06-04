# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <gogogo.vm@gmail.com>
"""

from __future__ import absolute_import
import abc

import six

from ._core import IntegerConverter
from ._core import FloatConverter
from ._core import DateTimeConverter


@six.add_metaclass(abc.ABCMeta)
class ValueConverterCreatorInterface(object):

    @abc.abstractmethod
    def create(self, value, is_convert):   # pragma: no cover
        pass


class IntegerConverterCreator(ValueConverterCreatorInterface):

    def create(self, value, is_convert):
        return IntegerConverter(value, is_convert)


class FloatConverterCreator(ValueConverterCreatorInterface):

    def create(self, value, is_convert):
        return FloatConverter(value, is_convert)


class DateTimeConverterCreator(ValueConverterCreatorInterface):

    def create(self, value, is_convert):
        return DateTimeConverter(value, is_convert)
