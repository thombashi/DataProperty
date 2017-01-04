# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <gogogo.vm@gmail.com>
"""

from __future__ import absolute_import
from __future__ import unicode_literals

from ._common import (
    DEFAULT_TYPE_VALUE_MAPPING,
    DEFAULT_CONST_VALUE_MAPPING,
    STRICT_TYPE_MAPPING,
    default_datetime_formatter,
)
from ._dataproperty import DataProperty
from ._error import TypeConversionError
from ._typecode import Typecode


class DataPropertyConverter(object):

    def __init__(
            self, type_value_mapping=None, const_value_mapping=None,
            datetime_formatter=default_datetime_formatter,
            float_type=None, strict_type_mapping=None):
        self.__type_value_mapping = (
            type_value_mapping
            if type_value_mapping else DEFAULT_TYPE_VALUE_MAPPING)
        self.__const_value_mapping = (
            const_value_mapping
            if const_value_mapping else DEFAULT_CONST_VALUE_MAPPING)
        self.__datetime_formatter = datetime_formatter
        self.__float_type = float_type
        self.__strict_type_mapping = strict_type_mapping

    def convert(self, dp_value):
        try:
            return DataProperty(
                self.__convert_value(dp_value),
                float_type=self.__float_type,
                strict_type_mapping=STRICT_TYPE_MAPPING)
        except TypeConversionError:
            return dp_value

    def __convert_value(self, dp_value):
        if dp_value.typecode in (Typecode.BOOL, Typecode.STRING):
            try:
                if dp_value.data in self.__const_value_mapping:
                    return self.__const_value_mapping.get(dp_value.data)
            except TypeError:
                # unhashable type will be reached this line
                raise TypeConversionError

        if dp_value.typecode in self.__type_value_mapping:
            return self.__type_value_mapping.get(
                dp_value.typecode,
                DEFAULT_TYPE_VALUE_MAPPING.get(dp_value.typecode))

        if dp_value.typecode == Typecode.DATETIME:
            try:
                return self.__datetime_formatter(dp_value.data)
            except TypeError:
                raise TypeConversionError

        raise TypeConversionError("no need to convert")
