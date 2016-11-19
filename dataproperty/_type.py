# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <gogogo.vm@gmail.com>
"""

from __future__ import absolute_import
import abc

from ._converter import ValueConverterInterface
from ._factory import (
    NoneTypeFactory,
    StringTypeFactory,
    IntegerTypeFactory,
    FloatTypeFactory,
    DateTimeTypeFactory,
    BoolTypeFactory,
    InfinityTypeFactory,
    NanTypeFactory,
    DictionaryTypeFactory
)
from ._type_checker import TypeCheckerInterface


class BaseType(TypeCheckerInterface, ValueConverterInterface):
    __slots__ = ("__checker", "__converter")

    @abc.abstractproperty
    def _factory_class(self):  # pragma: no cover
        pass

    def __init__(self, data, is_strict=False):
        factory = self._factory_class(data, is_strict)
        self.__checker = factory.create_type_checker()
        self.__converter = factory.create_type_converter()

    @property
    def typecode(self):
        return self.__checker.typecode

    def is_type(self):
        return self.__checker.is_type()

    def is_strict_type(self):
        return self.__checker.is_strict_type()

    def is_convertible_type(self):
        return self.__checker.is_convertible_type()

    def validate(self):
        return self.__checker.validate()

    def convert(self):
        return self.__converter.convert()

    def try_convert(self):
        return self.__converter.try_convert()


class NoneType(BaseType):

    @property
    def _factory_class(self):
        return NoneTypeFactory


class StringType(BaseType):

    @property
    def _factory_class(self):
        return StringTypeFactory


class IntegerType(BaseType):

    @property
    def _factory_class(self):
        return IntegerTypeFactory


class FloatType(BaseType):

    @property
    def _factory_class(self):
        return FloatTypeFactory


class DateTimeType(BaseType):

    @property
    def _factory_class(self):
        return DateTimeTypeFactory


class BoolType(BaseType):

    @property
    def _factory_class(self):
        return BoolTypeFactory


class InfinityType(BaseType):

    @property
    def _factory_class(self):
        return InfinityTypeFactory


class NanType(BaseType):

    @property
    def _factory_class(self):
        return NanTypeFactory


class DictionaryType(BaseType):

    @property
    def _factory_class(self):
        return DictionaryTypeFactory
