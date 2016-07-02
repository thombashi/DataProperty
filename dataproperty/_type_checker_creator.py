# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <gogogo.vm@gmail.com>
"""

from __future__ import absolute_import
import abc

import six

from ._type_checker import NoneTypeChecker
from ._type_checker import IntegerTypeChecker
from ._type_checker import FloatTypeChecker
from ._type_checker import BoolTypeChecker
from ._type_checker import DateTimeTypeChecker
from ._type_checker import InfinityChecker
from ._type_checker import NanChecker


@six.add_metaclass(abc.ABCMeta)
class TypeCheckerCreatorInterface(object):

    @abc.abstractmethod
    def create(self, value, is_convert):   # pragma: no cover
        pass


class NoneTypeCheckerCreator(TypeCheckerCreatorInterface):

    def create(self, value, is_convert):
        return NoneTypeChecker(value, is_convert)


class IntegerTypeCheckerCreator(TypeCheckerCreatorInterface):

    def create(self, value, is_convert):
        return IntegerTypeChecker(value, is_convert)


class FloatTypeCheckerCreator(TypeCheckerCreatorInterface):

    def create(self, value, is_convert):
        return FloatTypeChecker(value, is_convert)


class BoolTypeCheckerCreator(TypeCheckerCreatorInterface):

    def create(self, value, is_convert):
        return BoolTypeChecker(value, is_convert)


class DateTimeTypeCheckerCreator(TypeCheckerCreatorInterface):

    def create(self, value, is_convert):
        return DateTimeTypeChecker(value, is_convert)


class InfinityCheckerCreator(TypeCheckerCreatorInterface):

    def create(self, value, is_convert):
        return InfinityChecker(value, is_convert)


class NanCheckerCreator(TypeCheckerCreatorInterface):

    def create(self, value, is_convert):
        return NanChecker(value, is_convert)
