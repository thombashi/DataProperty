# encoding: utf-8

from __future__ import absolute_import, unicode_literals

import math
from decimal import Decimal

import six
from mbstrdecoder import MultiByteStrDecoder
from typepy import Integer, Nan, StrictLevel, Typecode, TypeConversionError

from ._align_getter import align_getter
from ._base import DataPeropertyBase
from ._common import DefaultValue
from ._container import ListContainer, MinMaxContainer
from ._function import calc_ascii_char_width


class ColumnDataProperty(DataPeropertyBase):
    __slots__ = (
        "__header_ascii_char_width",
        "__body_ascii_char_width",
        "__column_index",
        "__dp_list",
        "__format_map",
        "__is_calculate",
        "__minmax_integer_digits",
        "__minmax_decimal_places",
        "__minmax_additional_format_len",
        "__typecode_bitmap",
    )

    @property
    def align(self):
        return align_getter.get_align_from_typecode(self.typecode)

    @property
    def bit_length(self):
        if self.typecode != Typecode.INTEGER:
            return None

        bit_length = 0
        for value_dp in self.__dp_list:
            try:
                bit_length = max(bit_length, int.bit_length(value_dp.data))
            except TypeError:
                pass

        return bit_length

    @property
    def column_index(self):
        return self.__column_index

    @property
    def decimal_places(self):
        return self._decimal_places

    @property
    def ascii_char_width(self):
        return max(self.__header_ascii_char_width, self.__body_ascii_char_width)

    @property
    def minmax_integer_digits(self):
        return self.__minmax_integer_digits

    @property
    def minmax_decimal_places(self):
        return self.__minmax_decimal_places

    @property
    def minmax_additional_format_len(self):
        return self.__minmax_additional_format_len

    def __init__(
        self,
        column_index=None,
        min_width=0,
        format_flags=None,
        is_formatting_float=True,
        datetime_format_str=DefaultValue.DATETIME_FORMAT,
        east_asian_ambiguous_width=1,
    ):
        super(ColumnDataProperty, self).__init__(
            format_flags=format_flags,
            is_formatting_float=is_formatting_float,
            datetime_format_str=datetime_format_str,
            east_asian_ambiguous_width=east_asian_ambiguous_width,
        )

        self.__header_ascii_char_width = 0
        self.__body_ascii_char_width = min_width
        self.__column_index = column_index

        self.__is_calculate = True
        self.__dp_list = []
        self.__minmax_integer_digits = MinMaxContainer()
        self.__minmax_decimal_places = ListContainer()
        self.__minmax_additional_format_len = MinMaxContainer()

        self.__typecode_bitmap = Typecode.NONE.value
        self.__calc_typecode_from_bitmap()

        self.__format_map = self._formatter.make_format_map(decimal_places=self._decimal_places)

    def __repr__(self):
        element_list = []

        if self.column_index is not None:
            element_list.append("column={}".format(self.column_index))

        element_list.extend(
            [
                "type={}".format(self.typename),
                "align={}".format(self.align.align_string),
                "ascii_width={}".format(six.text_type(self.ascii_char_width)),
            ]
        )

        if Integer(self.bit_length).is_type():
            element_list.append("bit_len={:d}".format(self.bit_length))

        if self.minmax_integer_digits.has_value():
            if self.minmax_integer_digits.is_same_value():
                value = "int_digits={}".format(self.minmax_integer_digits.min_value)
            else:
                value = "int_digits=({})".format(self.minmax_integer_digits)

            element_list.append(value)

        if self.minmax_decimal_places.has_value():
            if self.minmax_decimal_places.is_same_value():
                value = "decimal_places={}".format(self.minmax_decimal_places.min_value)
            else:
                value = "decimal_places=({})".format(self.minmax_decimal_places)

            element_list.append(value)

        if not self.minmax_additional_format_len.is_zero():
            if self.minmax_additional_format_len.is_same_value():
                value = "extra_len={}".format(self.minmax_additional_format_len.min_value)
            else:
                value = "extra_len=({})".format(self.minmax_additional_format_len)

            element_list.append(value)

        return ", ".join(element_list)

    def dp_to_str(self, value_dp):
        try:
            value = self.__preprocess_value_before_tostring(value_dp)
        except TypeConversionError:
            return self.__format_map.get(value_dp.typecode, "{:s}").format(value_dp.data)

        to_string_format_str = self.__get_tostring_format(value_dp)

        try:
            return to_string_format_str.format(value)
        except ValueError:
            pass

        return MultiByteStrDecoder(value).unicode_str

    def extend_width(self, ascii_char_width):
        self.extend_header_width(ascii_char_width)
        self.extend_body_width(ascii_char_width)

    def extend_header_width(self, ascii_char_width):
        self.__header_ascii_char_width += ascii_char_width

    def extend_body_width(self, ascii_char_width):
        self.__body_ascii_char_width += ascii_char_width

    def update_header(self, header_db):
        self.__header_ascii_char_width = header_db.ascii_char_width

    def update_body(self, value_dp):
        if value_dp.is_include_ansi_escape:
            value_dp = value_dp.no_ansi_escape_dp

        self.__typecode_bitmap |= value_dp.typecode.value
        self.__calc_typecode_from_bitmap()

        if value_dp.typecode in (Typecode.REAL_NUMBER, Typecode.INTEGER):
            self.__minmax_integer_digits.update(value_dp.integer_digits)
            self.__minmax_decimal_places.update(value_dp.decimal_places)
            self.__calc_decimal_places()

        self.__minmax_additional_format_len.update(value_dp.additional_format_len)

        self.__dp_list.append(value_dp)
        self.__body_ascii_char_width = max(self.__body_ascii_char_width, value_dp.ascii_char_width)
        self.__calc_ascii_char_width()

    def merge(self, column_dp):
        self.__typecode_bitmap |= column_dp.typecode.value
        self.__calc_typecode_from_bitmap()

        self.__minmax_integer_digits.merge(column_dp.minmax_integer_digits)
        self.__minmax_decimal_places.update(column_dp.minmax_decimal_places)
        self.__calc_decimal_places()

        self.__minmax_additional_format_len.merge(column_dp.minmax_additional_format_len)

        self.__body_ascii_char_width = max(self.__body_ascii_char_width, column_dp.ascii_char_width)
        self.__calc_ascii_char_width()

    def begin_update(self):
        self.__is_calculate = False

    def end_update(self):
        self.__is_calculate = True

        self.__calc_typecode_from_bitmap()
        self.__calc_decimal_places()
        self.__calc_ascii_char_width()

    def __is_not_single_typecode(self, typecode_bitmap):
        return (
            self.__typecode_bitmap & typecode_bitmap and self.__typecode_bitmap & ~typecode_bitmap
        )

    def __is_float_typecode(self):
        FLOAT_TYPECODE_BMP = (
            Typecode.REAL_NUMBER.value | Typecode.INFINITY.value | Typecode.NAN.value
        )
        NUMBER_TYPECODE_BMP = FLOAT_TYPECODE_BMP | Typecode.INTEGER.value

        if self.__is_not_single_typecode(NUMBER_TYPECODE_BMP | Typecode.NULL_STRING.value):
            return False

        if (
            bin(self.__typecode_bitmap & (FLOAT_TYPECODE_BMP | Typecode.NULL_STRING.value)).count(
                "1"
            )
            >= 2
        ):
            return True

        if bin(self.__typecode_bitmap & NUMBER_TYPECODE_BMP).count("1") >= 2:
            return True

        return False

    def __update_body_ascii_char_width(self):
        if not self.__typecode_bitmap & (Typecode.REAL_NUMBER.value | Typecode.INTEGER.value):
            return self.__body_ascii_char_width

        max_width = self.__body_ascii_char_width

        for value_dp in self.__dp_list:
            if value_dp.typecode in [Typecode.INFINITY, Typecode.NAN]:
                continue

            if value_dp.is_include_ansi_escape:
                value_dp = value_dp.no_ansi_escape_dp

            max_width = max(
                max_width,
                calc_ascii_char_width(self.dp_to_str(value_dp), self._east_asian_ambiguous_width),
            )

        return max_width

    def __get_decimal_places(self):
        try:
            avg = self.minmax_decimal_places.mean()
        except TypeError:
            return None

        if Nan(avg).is_type():
            return None

        return int(min(math.ceil(avg + Decimal("1.0")), self.minmax_decimal_places.max_value))

    def __get_tostring_format(self, value_dp):
        if self.typecode == Typecode.STRING:
            return self.__format_map.get(value_dp.typecode, "{:s}")

        return self.__format_map.get(self.typecode, "{:s}")

    def __get_typecode_from_bitmap(self):
        if self.__is_float_typecode():
            return Typecode.REAL_NUMBER

        if any(
            [
                self.__is_not_single_typecode(Typecode.BOOL.value),
                self.__is_not_single_typecode(Typecode.DATETIME.value),
            ]
        ):
            return Typecode.STRING

        typecode_list = [
            Typecode.STRING,
            Typecode.REAL_NUMBER,
            Typecode.INTEGER,
            Typecode.DATETIME,
            Typecode.DICTIONARY,
            Typecode.IP_ADDRESS,
            Typecode.LIST,
            Typecode.BOOL,
            Typecode.INFINITY,
            Typecode.NAN,
            Typecode.NULL_STRING,
        ]

        for typecode in typecode_list:
            if self.__typecode_bitmap & typecode.value:
                return typecode

        if self.__typecode_bitmap == Typecode.NONE.value:
            return Typecode.NONE

        return Typecode.STRING

    def __calc_ascii_char_width(self):
        if not self.__is_calculate:
            return

        self.__body_ascii_char_width = self.__update_body_ascii_char_width()

    def __calc_decimal_places(self):
        if not self.__is_calculate:
            return

        self._decimal_places = self.__get_decimal_places()
        self.__format_map = self._formatter.make_format_map(decimal_places=self._decimal_places)

    def __calc_typecode_from_bitmap(self):
        if not self.__is_calculate:
            return

        self._typecode = self.__get_typecode_from_bitmap()

    def __preprocess_value_before_tostring(self, value_dp):
        if self.typecode == value_dp.typecode or self.typecode in [
            Typecode.STRING,
            Typecode.BOOL,
            Typecode.DATETIME,
        ]:
            return value_dp.data

        return self.type_class(
            value_dp.data, strict_level=StrictLevel.MIN, strip_ansi_escape=False
        ).convert()
