# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <gogogo.vm@gmail.com>
"""

from __future__ import absolute_import
import abc

import six

from ._type_checker import IntegerTypeChecker
from ._type_checker import FloatTypeChecker
from ._type_checker import DateTimeTypeChecker


@six.add_metaclass(abc.ABCMeta)
class TypeCheckerCreatorInterface(object):

    @abc.abstractmethod
    def create(self, value, is_convert):   # pragma: no cover
        pass


class IntegerTypeCheckerCreator(TypeCheckerCreatorInterface):

    def create(self, value, is_convert):
        return IntegerTypeChecker(value, is_convert)


class FloatTypeCheckerCreator(TypeCheckerCreatorInterface):

    def create(self, value, is_convert):
        return FloatTypeChecker(value, is_convert)


class DateTimeTypeCheckerCreator(TypeCheckerCreatorInterface):

    def create(self, value, is_convert):
        return DateTimeTypeChecker(value, is_convert)
