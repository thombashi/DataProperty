# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <gogogo.vm@gmail.com>
"""

from __future__ import absolute_import
import abc

import six

from ._error import TypeConversionError


@six.add_metaclass(abc.ABCMeta)
class TypeCheckerInterface(object):

    @abc.abstractmethod
    def is_type(self):
        pass


class TypeChecker(TypeCheckerInterface):

    def __init__(self, value, is_convert=True):
        self._value = value
        self._converted_value = None
        self._is_convert = is_convert

    def is_type(self):
        if self._is_instance():
            return True

        if self._is_exclude_instance():
            return False

        if not self._is_convert:
            return False

        try:
            self._try_convert()
        except TypeConversionError:
            return False

        if not self._is_valid_after_convert():
            return False

        return True

    @abc.abstractmethod
    def _is_instance(self):
        pass

    @abc.abstractmethod
    def _is_exclude_instance(self):
        pass

    @abc.abstractmethod
    def _try_convert(self):
        pass

    @abc.abstractmethod
    def _is_valid_after_convert(self):
        pass


class IntegerTypeChecker(TypeChecker):

    def _is_instance(self):
        if isinstance(self._value, six.integer_types):
            return not isinstance(self._value, bool)

        return False

    def _is_exclude_instance(self):
        return any([
            isinstance(self._value, bool),
            isinstance(self._value, float),
        ])

    def _try_convert(self):
        try:
            self._converted_value = int(self._value)
        except (TypeError, ValueError):
            raise TypeConversionError

    def _is_valid_after_convert(self):
        return True


class FloatTypeChecker(TypeChecker):

    def _is_instance(self):
        return any(
            [isinstance(self._value, float), self._value == float("inf")])

    def _is_exclude_instance(self):
        return isinstance(self._value, bool)

    def _try_convert(self):
        try:
            self._converted_value = float(self._value)
        except (TypeError, ValueError):
            raise TypeConversionError

    def _is_valid_after_convert(self):
        return self._converted_value != float("inf")
