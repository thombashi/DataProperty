# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <gogogo.vm@gmail.com>
"""

from __future__ import absolute_import
import abc

import six

from ._core import NopConverter
from ._core import StringConverter
from ._core import IntegerConverter
from ._core import FloatConverter
from ._core import BoolConverter
from ._core import DateTimeConverter


@six.add_metaclass(abc.ABCMeta)
class ValueConverterCreatorInterface(object):

    @abc.abstractmethod
    def create(self, value):  # pragma: no cover
        pass


class NopConverterCreator(ValueConverterCreatorInterface):

    def create(self, value):
        return NopConverter(value)


class StringConverterCreator(ValueConverterCreatorInterface):

    def create(self, value):
        return StringConverter(value)


class IntegerConverterCreator(ValueConverterCreatorInterface):

    def create(self, value):
        return IntegerConverter(value)


class FloatConverterCreator(ValueConverterCreatorInterface):

    def create(self, value):
        return FloatConverter(value)


class BoolConverterCreator(ValueConverterCreatorInterface):

    def create(self, value):
        return BoolConverter(value)


class DateTimeConverterCreator(ValueConverterCreatorInterface):

    def create(self, value):
        return DateTimeConverter(value)
