# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <gogogo.vm@gmail.com>
"""

from __future__ import absolute_import
from __future__ import unicode_literals
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


class AbstractType(TypeCheckerInterface, ValueConverterInterface):
    __slots__ = ("__checker", "__converter")

    @abc.abstractproperty
    def _factory_class(self):  # pragma: no cover
        pass

    def __init__(self, data, is_strict=False, params=None):
        if params is None:
            params = {}

        factory = self._factory_class(data, is_strict, params)
        self.__checker = factory.create_type_checker()
        self.__converter = factory.create_type_converter()

    @property
    def typecode(self):
        return self.__checker.typecode

    def __repr__(self):
        element_list = [
            "is_type={}".format(self.is_type()),
            "is_strict_type={}".format(self.is_strict_type()),
            "is_convertible_type={}".format(self.is_convertible_type()),
            "try_convert={}".format(self.try_convert()),
        ]

        return ", ".join(element_list)

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


class NoneType(AbstractType):

    @property
    def _factory_class(self):
        return NoneTypeFactory


class StringType(AbstractType):

    @property
    def _factory_class(self):
        return StringTypeFactory


class IntegerType(AbstractType):

    @property
    def _factory_class(self):
        return IntegerTypeFactory


class FloatType(AbstractType):

    @property
    def _factory_class(self):
        return FloatTypeFactory


class DateTimeType(AbstractType):

    @property
    def _factory_class(self):
        return DateTimeTypeFactory


class BoolType(AbstractType):

    @property
    def _factory_class(self):
        return BoolTypeFactory


class InfinityType(AbstractType):

    @property
    def _factory_class(self):
        return InfinityTypeFactory


class NanType(AbstractType):

    @property
    def _factory_class(self):
        return NanTypeFactory


class DictionaryType(AbstractType):

    @property
    def _factory_class(self):
        return DictionaryTypeFactory
