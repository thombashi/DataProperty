# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <gogogo.vm@gmail.com>
"""

from __future__ import absolute_import
import abc

import six

from .converter import NopConverterCreator
from .converter import StringConverterCreator
from .converter import IntegerConverterCreator
from .converter import FloatConverterCreator
from .converter import BoolConverterCreator
from .converter import DateTimeConverterCreator
from .type import NoneTypeCheckerCreator
from .type import StringTypeCheckerCreator
from .type import IntegerTypeCheckerCreator
from .type import FloatTypeCheckerCreator
from .type import BoolTypeCheckerCreator
from .type import DateTimeTypeCheckerCreator
from .type import InfinityCheckerCreator
from .type import NanCheckerCreator


@six.add_metaclass(abc.ABCMeta)
class TypeConverterFactoryInterface(object):
    """
    Abstract factory class of type converter.
    """

    @abc.abstractproperty
    def type_checker_factory(self):  # pragma: no cover
        pass

    @abc.abstractproperty
    def value_converter_factory(self):  # pragma: no cover
        pass


class NoneTypeFactory(TypeConverterFactoryInterface):

    @property
    def type_checker_factory(self):
        return NoneTypeCheckerCreator()

    @property
    def value_converter_factory(self):
        return NopConverterCreator()


class StringTypeFactory(TypeConverterFactoryInterface):

    @property
    def type_checker_factory(self):
        return StringTypeCheckerCreator()

    @property
    def value_converter_factory(self):
        return StringConverterCreator()


class IntegerTypeFactory(TypeConverterFactoryInterface):

    @property
    def type_checker_factory(self):
        return IntegerTypeCheckerCreator()

    @property
    def value_converter_factory(self):
        return IntegerConverterCreator()


class FloatTypeFactory(TypeConverterFactoryInterface):

    @property
    def type_checker_factory(self):
        return FloatTypeCheckerCreator()

    @property
    def value_converter_factory(self):
        return FloatConverterCreator()


class DateTimeTypeFactory(TypeConverterFactoryInterface):

    @property
    def type_checker_factory(self):
        return DateTimeTypeCheckerCreator()

    @property
    def value_converter_factory(self):
        return DateTimeConverterCreator()


class BoolTypeFactory(TypeConverterFactoryInterface):

    @property
    def type_checker_factory(self):
        return BoolTypeCheckerCreator()

    @property
    def value_converter_factory(self):
        return BoolConverterCreator()


class InfinityTypeFactory(TypeConverterFactoryInterface):

    @property
    def type_checker_factory(self):
        return InfinityCheckerCreator()

    @property
    def value_converter_factory(self):
        return FloatConverterCreator()


class NanTypeFactory(TypeConverterFactoryInterface):

    @property
    def type_checker_factory(self):
        return NanCheckerCreator()

    @property
    def value_converter_factory(self):
        return FloatConverterCreator()
