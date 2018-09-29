# encoding: utf-8

from __future__ import absolute_import, unicode_literals

import copy

from typepy import (
    DateTime,
    Dictionary,
    Infinity,
    Integer,
    IpAddress,
    List,
    Nan,
    NoneType,
    NullString,
    RealNumber,
    String,
    Typecode,
)


class FormatFlag(object):
    NONE = 0
    THOUSAND_SEPARATOR = 1


class Formatter(object):
    __slots__ = ("__is_formatting_float", "__format_flag", "__datetime_format_str")

    _BLANK_CURLY_BRACES_FORMAT_MAPPING = {
        Typecode.NONE: "{}",
        Typecode.IP_ADDRESS: "{}",
        Typecode.BOOL: "{}",
        Typecode.DICTIONARY: "{}",
        Typecode.LIST: "{}",
    }

    @property
    def blank_curly_braces_format_type_list(self):
        return self._BLANK_CURLY_BRACES_FORMAT_MAPPING.keys()

    def __init__(self, format_flag, datetime_format_str, is_formatting_float=True):
        self.__format_flag = format_flag
        self.__datetime_format_str = datetime_format_str
        self.__is_formatting_float = is_formatting_float

    def make_format_mapping(self, decimal_places=None):
        format_mapping = copy.copy(self._BLANK_CURLY_BRACES_FORMAT_MAPPING)
        format_mapping.update(
            {
                Typecode.INTEGER: self.make_format_str(Typecode.INTEGER),
                Typecode.REAL_NUMBER: self.make_format_str(Typecode.REAL_NUMBER, decimal_places),
                Typecode.INFINITY: self.make_format_str(Typecode.INFINITY),
                Typecode.NAN: self.make_format_str(Typecode.NAN),
                Typecode.DATETIME: self.make_format_str(Typecode.DATETIME),
            }
        )

        return format_mapping

    def make_format_str(self, typecode, decimal_places=None):
        format_str = self._BLANK_CURLY_BRACES_FORMAT_MAPPING.get(typecode)
        if format_str is not None:
            return format_str

        if typecode == Typecode.INTEGER:
            return "{:d}"

        if typecode in (Typecode.REAL_NUMBER, Typecode.INFINITY, Typecode.NAN):
            return self.__get_realnumber_format(decimal_places)

        if typecode == Typecode.DATETIME:
            return "{:" + self.__datetime_format_str + "}"

        return "{:s}"

    def __get_integer_format(self):
        return "{:d}"

    def __get_realnumber_format(self, decimal_places):
        if not self.__is_formatting_float:
            return "{}"

        if decimal_places is None or Nan(decimal_places).is_type():
            return "{:f}"

        try:
            return "{:" + ".{:d}f".format(decimal_places) + "}"
        except ValueError:
            return "{:f}"
