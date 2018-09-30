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

from ._formatter import Formatter
from ._interface import DataPeropertyInterface


class DataPeropertyBase(DataPeropertyInterface):
    __slots__ = (
        "_datetime_format_str",
        "_decimal_places",
        "_east_asian_ambiguous_width",
        "_formatter",
        "_typecode",
        "__format_str",
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

        self.__format_str = self._formatter.make_format_str(self.typecode, self.decimal_places)

        return self.__format_str

    def __init__(
        self, format_flags, is_formatting_float, datetime_format_str, east_asian_ambiguous_width
    ):
        self._decimal_places = None
        self._east_asian_ambiguous_width = east_asian_ambiguous_width
        self._typecode = None

        self._datetime_format_str = datetime_format_str
        self.__format_str = None

        self._formatter = Formatter(
            format_flags=format_flags,
            datetime_format_str=self._datetime_format_str,
            is_formatting_float=is_formatting_float,
        )
