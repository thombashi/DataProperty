# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <gogogo.vm@gmail.com>
"""

from __future__ import absolute_import
from __future__ import unicode_literals
import abc
from decimal import Decimal
import math

import six

from ._converter import (
    NopConverter,
    StringConverter,
    IntegerConverter,
    FloatConverter,
    BoolConverter,
    DateTimeConverter,
    DictionaryConverter,
)
from ._typecode import Typecode


@six.add_metaclass(abc.ABCMeta)
class TypeCheckerInterface(object):

    @abc.abstractproperty
    def typecode(self):  # pragma: no cover
        pass

    @abc.abstractmethod
    def is_type(self):  # pragma: no cover
        pass

    @abc.abstractmethod
    def is_strict_type(self):  # pragma: no cover
        pass

    @abc.abstractmethod
    def is_convertible_type(self):  # pragma: no cover
        pass

    @abc.abstractmethod
    def validate(self):  # pragma: no cover
        pass


class TypeChecker(TypeCheckerInterface):
    __slots__ = (
        "_value",
        "_converted_value",
        "__is_strict",
        "__converter"
    )

    @abc.abstractproperty
    def _converter_class(self):  # pragma: no cover
        pass

    def __init__(self, value, is_strict=False):
        self._value = value
        self._converted_value = None
        self.__is_strict = is_strict
        self.__converter = self._converter_class(value)

    def is_type(self):
        __CHECKER_TABLE = {
            True: self.is_strict_type,
            False: self.is_convertible_type,
        }

        return __CHECKER_TABLE[self.__is_strict]()

    def is_strict_type(self):
        return self._is_instance()

    def is_convertible_type(self):
        if self.is_strict_type():
            return True

        if self._is_exclude_instance():
            return False

        self._converted_value = self.__converter.try_convert()
        if self._converted_value is None:
            return False

        if not self._is_valid_after_convert():
            return False

        return True

    def validate(self):
        """
        :raises TypeError:
            If the value is not matched the type to be expected.
        """

        if self.is_type():
            return

        raise TypeError(
            "invalid value type: expected-type={:s}".format(
                Typecode.get_typename(self.typecode)))

    @abc.abstractmethod
    def _is_instance(self):
        pass

    def _is_exclude_instance(self):
        return False

    def _is_valid_after_convert(self):
        return True


class NoneTypeChecker(TypeChecker):

    @property
    def typecode(self):
        return Typecode.NONE

    @property
    def _converter_class(self):
        return NopConverter

    def _is_instance(self):
        return self._value is None

    def _is_valid_after_convert(self):
        return self._value is None


class StringTypeChecker(TypeChecker):

    @property
    def typecode(self):
        return Typecode.STRING

    @property
    def _converter_class(self):
        return StringConverter

    def _is_instance(self):
        return self.__is_string(self._value)

    def _is_valid_after_convert(self):
        return self.__is_string(self._converted_value)

    @staticmethod
    def __is_string(value):
        return any([
            isinstance(value, six.string_types),
            isinstance(value, six.binary_type),
        ])


class IntegerTypeChecker(TypeChecker):
    """
    is_type() behave differently from float.is_integer()

    examples:
    """

    @property
    def typecode(self):
        return Typecode.INTEGER

    @property
    def _converter_class(self):
        return IntegerConverter

    def _is_instance(self):
        if isinstance(self._value, six.integer_types):
            return not isinstance(self._value, bool)

        if isinstance(self._value, float) or isinstance(self._value, Decimal):
            if float(self._value).is_integer():
                return True

        try:
            return self._value.is_integer()
        except AttributeError:
            pass

        return False

    def _is_exclude_instance(self):
        return any([
            isinstance(self._value, bool),
            isinstance(self._value, float),
            isinstance(self._value, Decimal),
        ])


class FloatTypeChecker(TypeChecker):

    @property
    def typecode(self):
        return Typecode.FLOAT

    @property
    def _converter_class(self):
        return FloatConverter

    def _is_instance(self):
        return any([
            isinstance(self._value, float),
            isinstance(self._value, Decimal),
        ])

    def _is_exclude_instance(self):
        return isinstance(self._value, bool)


class BoolTypeChecker(TypeChecker):

    @property
    def typecode(self):
        return Typecode.BOOL

    @property
    def _converter_class(self):
        return BoolConverter

    def _is_instance(self):
        return isinstance(self._value, bool)

    def _is_valid_after_convert(self):
        return isinstance(self._converted_value, bool)


class DateTimeTypeChecker(TypeChecker):

    @property
    def typecode(self):
        return Typecode.DATETIME

    @property
    def _converter_class(self):
        return DateTimeConverter

    def _is_instance(self):
        import datetime

        return isinstance(self._value, datetime.datetime)


class InfinityChecker(TypeChecker):

    @property
    def typecode(self):
        return Typecode.INFINITY

    @property
    def _converter_class(self):
        return FloatConverter

    def _is_instance(self):
        return self._value in (float("inf"), Decimal("inf"))

    def _is_valid_after_convert(self):
        return self._converted_value.is_infinite()


class NanChecker(TypeChecker):

    @property
    def typecode(self):
        return Typecode.NAN

    @property
    def _converter_class(self):
        return FloatConverter

    def _is_instance(self):
        try:
            return math.isnan(self._value)
        except TypeError:
            return False

    def _is_valid_after_convert(self):
        return math.isnan(self._converted_value)


class DictionaryTypeChecker(TypeChecker):

    @property
    def typecode(self):
        return Typecode.DICTIONARY

    @property
    def _converter_class(self):
        return DictionaryConverter

    def _is_instance(self):
        return isinstance(self._value, dict)
