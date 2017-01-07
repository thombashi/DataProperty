# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <gogogo.vm@gmail.com>
"""

from __future__ import absolute_import
import abc

import six

from ._common import DefaultValue
from ._type_checker import (
    NoneTypeChecker,
    StringTypeChecker,
    NullStringTypeChecker,
    IntegerTypeChecker,
    FloatTypeChecker,
    BoolTypeChecker,
    DateTimeTypeChecker,
    InfinityChecker,
    NanChecker,
    DictionaryTypeChecker,
)
from ._type_converter import (
    NopConverter,
    StringConverter,
    NullStringConverter,
    IntegerConverter,
    FloatConverter,
    BoolConverter,
    DateTimeConverter,
    DictionaryConverter,
)


@six.add_metaclass(abc.ABCMeta)
class TypeFactoryInterface(object):
    """
    Abstract factory class of type converter.
    """

    @abc.abstractmethod
    def create_type_checker(self):  # pragma: no cover
        pass

    @abc.abstractmethod
    def create_type_converter(self):  # pragma: no cover
        pass


class AbstractTypeFactory(TypeFactoryInterface):
    __slots__ = ("_data", "_is_strict", "params")

    def __init__(self, data, is_strict, params=None):
        self._data = data
        self._is_strict = is_strict

        if params is None:
            self._params = {}
        else:
            self._params = params


class NoneTypeFactory(AbstractTypeFactory):

    def create_type_checker(self):
        return NoneTypeChecker(self._data, self._is_strict)

    def create_type_converter(self):
        return NopConverter(self._data)


class StringTypeFactory(AbstractTypeFactory):

    def create_type_checker(self):
        return StringTypeChecker(self._data, self._is_strict)

    def create_type_converter(self):
        return StringConverter(self._data)


class NullStringTypeFactory(AbstractTypeFactory):

    def create_type_checker(self):
        return NullStringTypeChecker(self._data, self._is_strict)

    def create_type_converter(self):
        return NullStringConverter(self._data)


class IntegerTypeFactory(AbstractTypeFactory):

    def create_type_checker(self):
        return IntegerTypeChecker(self._data, self._is_strict)

    def create_type_converter(self):
        return IntegerConverter(self._data)


class FloatTypeFactory(AbstractTypeFactory):

    def create_type_checker(self):
        return FloatTypeChecker(self._data, self._is_strict)

    def create_type_converter(self):
        converter = FloatConverter(self._data)
        converter.float_class = self._params.get(
            "float_type", DefaultValue.FLOAT_TYPE)

        return converter


class DateTimeTypeFactory(AbstractTypeFactory):

    def create_type_checker(self):
        return DateTimeTypeChecker(self._data, self._is_strict)

    def create_type_converter(self):
        return DateTimeConverter(self._data)


class BoolTypeFactory(AbstractTypeFactory):

    def create_type_checker(self):
        return BoolTypeChecker(self._data, self._is_strict)

    def create_type_converter(self):
        return BoolConverter(self._data)


class InfinityTypeFactory(AbstractTypeFactory):

    def create_type_checker(self):
        return InfinityChecker(self._data, self._is_strict)

    def create_type_converter(self):
        return FloatConverter(self._data)


class NanTypeFactory(AbstractTypeFactory):

    def create_type_checker(self):
        return NanChecker(self._data, self._is_strict)

    def create_type_converter(self):
        return FloatConverter(self._data)


class DictionaryTypeFactory(AbstractTypeFactory):

    def create_type_checker(self):
        return DictionaryTypeChecker(self._data, self._is_strict)

    def create_type_converter(self):
        return DictionaryConverter(self._data)
