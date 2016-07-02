# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <gogogo.vm@gmail.com>
"""

from __future__ import absolute_import
import abc

import six

from ._core import NopConverter
from ._core import IntegerConverter
from ._core import FloatConverter
from ._core import DateTimeConverter
from ._core import InfinityConverter


@six.add_metaclass(abc.ABCMeta)
class ValueConverterCreatorInterface(object):

    @abc.abstractmethod
    def create(self, value):   # pragma: no cover
        pass


class NoneConverterCreator(ValueConverterCreatorInterface):

    def create(self, value):
        return NopConverter(value)


class IntegerConverterCreator(ValueConverterCreatorInterface):

    def create(self, value):
        return IntegerConverter(value)


class FloatConverterCreator(ValueConverterCreatorInterface):

    def create(self, value):
        return FloatConverter(value)


class DateTimeConverterCreator(ValueConverterCreatorInterface):

    def create(self, value):
        return DateTimeConverter(value)


class InfinityConverterCreator(ValueConverterCreatorInterface):

    def create(self, value):
        return InfinityConverter(value)
