# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <gogogo.vm@gmail.com>
"""

from __future__ import absolute_import
import abc

import six

from ._function import is_nan
from ._typecode import Typecode


@six.add_metaclass(abc.ABCMeta)
class DataPeropertyInterface(object):
    __slots__ = ()

    @abc.abstractproperty
    def align(self):   # pragma: no cover
        pass

    @abc.abstractproperty
    def decimal_places(self):   # pragma: no cover
        pass

    @abc.abstractproperty
    def typecode(self):   # pragma: no cover
        pass

    @property
    def format_str(self):
        if self.typecode == Typecode.INT:
            return "d"

        if self.typecode == Typecode.FLOAT:
            if is_nan(self.decimal_places):
                return "f"

            return ".%df" % (self.decimal_places)

        return "s"
