# encoding: utf-8

from __future__ import absolute_import, unicode_literals

from typepy import (
    Bool,
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

from ._interface import DataPeropertyInterface


class DataPeropertyBase(DataPeropertyInterface):
    __slots__ = (
        "_east_asian_ambiguous_width",
        "_typecode",
        "__datetime_format_str",
        "__format_str",
        "__blank_curly_braces_format_types",
    )

    __TYPE_CLASS_TABLE = {
        Typecode.BOOL: Bool,
        Typecode.DATETIME: DateTime,
        Typecode.DICTIONARY: Dictionary,
        Typecode.INTEGER: Integer,
        Typecode.INFINITY: Infinity,
        Typecode.IP_ADDRESS: IpAddress,
        Typecode.LIST: List,
        Typecode.NAN: Nan,
        Typecode.NONE: NoneType,
        Typecode.NULL_STRING: NullString,
        Typecode.REAL_NUMBER: RealNumber,
        Typecode.STRING: String,
    }

    @property
    def type_class(self):
        return self.__TYPE_CLASS_TABLE.get(self.typecode)

    @property
    def typecode(self):
        """
        ``typepy.Typecode`` that corresponds to the type of the ``data``.

        :return:
            One of the Enum value that are defined ``typepy.Typecode``.
        :rtype: typepy.Typecode
        """

        return self._typecode

    @property
    def typename(self):
        return self.typecode.name

    @property
    def format_str(self):
        if self.__format_str:
            return self.__format_str

        self.__format_str = self.__get_format_str()

        return self.__format_str

    @property
    def __format_str_mapping(self):
        return {
            Typecode.NONE: "{}",
            Typecode.INTEGER: "{:d}",
            Typecode.IP_ADDRESS: "{}",
            Typecode.BOOL: "{}",
            Typecode.DATETIME: "{:" + self.__datetime_format_str + "}",
            Typecode.DICTIONARY: "{}",
            Typecode.LIST: "{}",
        }

    @property
    def _blank_curly_braces_format_types(self):
        if self.__blank_curly_braces_format_types:
            return self.__blank_curly_braces_format_types

        self.__blank_curly_braces_format_types = [
            typecode
            for typecode, format_str in self.__format_str_mapping.items()
            if format_str == "{}"
        ]

        return self.__blank_curly_braces_format_types

    def __init__(self, datetime_format_str, east_asian_ambiguous_width):
        self._east_asian_ambiguous_width = east_asian_ambiguous_width
        self._typecode = None

        self.__datetime_format_str = datetime_format_str
        self.__format_str = None
        self.__blank_curly_braces_format_types = None

    def __get_format_str(self):
        format_str = self.__format_str_mapping.get(self.typecode)

        if format_str is not None:
            return format_str

        if self.typecode in (Typecode.REAL_NUMBER, Typecode.INFINITY, Typecode.NAN):
            if Nan(self.decimal_places).is_type():
                return "{:f}"

            return self._get_realnumber_format()

        return "{:s}"

    def _get_realnumber_format(self):
        if self.decimal_places is None:
            return "{:f}"

        try:
            return "{:" + ".{:d}f".format(self.decimal_places) + "}"
        except ValueError:
            return "{:f}"
