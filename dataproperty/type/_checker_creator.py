# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <gogogo.vm@gmail.com>
"""

from __future__ import absolute_import
import abc

import six

from ._checker import NoneTypeChecker
from ._checker import StringTypeChecker
from ._checker import IntegerTypeChecker
from ._checker import FloatTypeChecker
from ._checker import BoolTypeChecker
from ._checker import DateTimeTypeChecker
from ._checker import InfinityChecker
from ._checker import NanChecker


@six.add_metaclass(abc.ABCMeta)
class TypeCheckerCreatorInterface(object):

    @abc.abstractmethod
    def create(self, value, is_convert):  # pragma: no cover
        pass


class NoneTypeCheckerCreator(TypeCheckerCreatorInterface):

    def create(self, value, is_convert):
        return NoneTypeChecker(value, is_convert)


class StringTypeCheckerCreator(TypeCheckerCreatorInterface):

    def create(self, value, is_convert):
        return StringTypeChecker(value, is_convert)


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
