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
from ._formatter import Formatter
from ._function import get_ascii_char_width


class ColumnDataProperty(DataPeropertyBase):
    __slots__ = (
        "__ascii_char_width",
        "__column_index",
        "__dp_list",
        "__formatter",
        "__format_mapping",
        "__is_calculate",
        "__is_formatting_float",
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
        return self.__ascii_char_width

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
        format_flag=None,
        is_formatting_float=True,
        datetime_format_str=DefaultValue.DATETIME_FORMAT,
        east_asian_ambiguous_width=1,
    ):
        super(ColumnDataProperty, self).__init__(
            datetime_format_str=datetime_format_str,
            east_asian_ambiguous_width=east_asian_ambiguous_width,
        )

        self.__ascii_char_width = min_width
        self.__column_index = column_index

        self.__is_calculate = True
        self.__is_formatting_float = is_formatting_float
        self.__dp_list = []
        self.__minmax_integer_digits = MinMaxContainer()
        self.__minmax_decimal_places = ListContainer()
        self.__minmax_additional_format_len = MinMaxContainer()

        self.__typecode_bitmap = Typecode.NONE.value
        self.__calc_typecode_from_bitmap()

        self.__formatter = Formatter(
            format_flag=None,
            datetime_format_str=self._datetime_format_str,
            is_formatting_float=self.__is_formatting_float,
        )
        self.__format_mapping = self.__formatter.make_format_mapping(
            decimal_places=self._decimal_places
        )

    def __repr__(self):
        element_list = []

        if self.column_index is not None:
            element_list.append("column={}".format(self.column_index))

        element_list.extend(
            [
                "typename={}".format(self.typename),
                "align={}".format(self.align.align_string),
                "ascii_char_width={}".format(six.text_type(self.ascii_char_width)),
            ]
        )

        if Integer(self.bit_length).is_type():
            element_list.append("bit_len={:d}".format(self.bit_length))

        if self.minmax_integer_digits.has_value():
            if self.minmax_integer_digits.is_same_value():
                value = "integer_digits={}".format(self.minmax_integer_digits.min_value)
            else:
                value = "integer_digits=({})".format(self.minmax_integer_digits)

            element_list.append(value)

        if self.minmax_decimal_places.has_value():
            if self.minmax_decimal_places.is_same_value():
                value = "decimal_places={}".format(self.minmax_decimal_places.min_value)
            else:
                value = "decimal_places=({})".format(self.minmax_decimal_places)

            element_list.append(value)

        if not self.minmax_additional_format_len.is_zero():
            if self.minmax_additional_format_len.is_same_value():
                value = "additional_format_len={}".format(
                    self.minmax_additional_format_len.min_value
                )
            else:
                value = "additional_format_len=({})".format(self.minmax_additional_format_len)

            element_list.append(value)

        return ", ".join(element_list)

    def dp_to_str(self, value_dp):
        try:
            value = self.__preprocess_value_before_tostring(value_dp)
        except TypeConversionError:
            return self.__format_mapping.get(value_dp.typecode, "{:s}").format(value_dp.data)

        to_string_format_str = self.__get_tostring_format(value_dp)

        try:
            return to_string_format_str.format(value)
        except ValueError:
            pass

        return MultiByteStrDecoder(value).unicode_str

    def extend_width(self, dwidth):
        self.__ascii_char_width += dwidth

    def update_header(self, dataprop):
        self.__ascii_char_width = max(self.__ascii_char_width, dataprop.ascii_char_width)

    def update_body(self, dataprop):
        self.__typecode_bitmap |= dataprop.typecode.value
        self.__calc_typecode_from_bitmap()

        if dataprop.typecode in (Typecode.REAL_NUMBER, Typecode.INTEGER):
            self.__minmax_integer_digits.update(dataprop.integer_digits)
            self.__minmax_decimal_places.update(dataprop.decimal_places)
            self.__calc_decimal_places()

        self.__minmax_additional_format_len.update(dataprop.additional_format_len)

        self.__dp_list.append(dataprop)
        self.__ascii_char_width = max(self.__ascii_char_width, dataprop.ascii_char_width)
        self.__calc_ascii_char_width()

    def merge(self, col_dataprop):
        self.__typecode_bitmap |= col_dataprop.typecode.value
        self.__calc_typecode_from_bitmap()

        self.__minmax_integer_digits.merge(col_dataprop.minmax_integer_digits)
        self.__minmax_decimal_places.update(col_dataprop.minmax_decimal_places)
        self.__calc_decimal_places()

        self.__minmax_additional_format_len.merge(col_dataprop.minmax_additional_format_len)

        self.__ascii_char_width = max(self.__ascii_char_width, col_dataprop.ascii_char_width)
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

    def __get_ascii_char_width(self):
        if not self.__typecode_bitmap & Typecode.REAL_NUMBER.value:
            return self.__ascii_char_width

        max_width = self.__ascii_char_width

        for value_dp in self.__dp_list:
            if value_dp.typecode in [Typecode.INFINITY, Typecode.NAN]:
                continue

            max_width = max(
                max_width,
                get_ascii_char_width(self.dp_to_str(value_dp), self._east_asian_ambiguous_width),
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
            return self.__format_mapping.get(value_dp.typecode, "{:s}")

        return self.__format_mapping.get(self.typecode, "{:s}")

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

        self.__ascii_char_width = self.__get_ascii_char_width()

    def __calc_decimal_places(self):
        if not self.__is_calculate:
            return

        self._decimal_places = self.__get_decimal_places()
        self.__format_mapping = self.__formatter.make_format_mapping(
            decimal_places=self._decimal_places
        )

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

        return self.type_class(value_dp.data, strict_level=StrictLevel.MIN).convert()