# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <gogogo.vm@gmail.com>
"""

from __future__ import absolute_import
import math

from ._align_getter import align_getter
from ._container import MinMaxContainer
from ._interface import DataPeropertyInterface
from ._typecode import Typecode

from ._function import convert_value
from ._function import is_float
from ._function import is_nan
from ._function import get_number_of_digit
from ._function import get_text_len


class DataProperty(DataPeropertyInterface):
    __slots__ = (
        "__data",
        "__typecode",
        "__align",
        "__integer_digits",
        "__decimal_places",
        "__additional_format_len",
        "__str_len",
    )

    @property
    def align(self):
        return self.__align

    @property
    def decimal_places(self):
        """
        :return:
            Decimal places if the ``data`` is ``float``.
            Returns ``0`` if the ``data`` is ``int``.
            Otherwise, returns ``float("nan")``.
        :rtype: int
        """

        return self.__decimal_places

    @property
    def typecode(self):
        """
        Return the type code that corresponds to the type of the ``data``.

        :return: One of the constants that are defined in the ``Typecode`` class.
        :rtype: int
        """

        return self.__typecode

    @property
    def format_str(self):
        if self.typecode == Typecode.INT:
            return "d"

        if self.typecode == Typecode.FLOAT:
            if is_nan(self.decimal_places):
                return "f"

            return ".%df" % (self.decimal_places)

        return "s"

    @property
    def data(self):
        """
        :return: Original data.
        :rtype: Original data type.
        """

        return self.__data

    @property
    def str_len(self):
        """
        :return: Length of the ``data`` as a string.
        :rtype: int
        """

        return self.__str_len

    @property
    def integer_digits(self):
        """
        :return:
            Integer digits if the ``data`` is ``int``/``float``.
            Otherwise, returns ``float("nan")``.
        :rtype: int
        """

        return self.__integer_digits

    @property
    def additional_format_len(self):
        return self.__additional_format_len

    def __init__(self, data, replace_tabs_with_spaces=True, tab_length=2):
        super(DataProperty, self).__init__()

        self.__set_data(data, replace_tabs_with_spaces, tab_length)
        self.__typecode = Typecode.get_typecode_from_data(data)
        self.__align = align_getter.get_align_from_typecode(self.typecode)

        integer_digits, decimal_places = get_number_of_digit(data)
        self.__integer_digits = integer_digits
        self.__decimal_places = decimal_places
        self.__additional_format_len = self.__get_additional_format_len()
        self.__str_len = self.__get_str_len()

    def __repr__(self):
        return ", ".join([
            ("data=%" + self.format_str) % (self.data),
            "typename=" + Typecode.get_typename(self.typecode),
            "align=" + str(self.align),
            "str_len=" + str(self.str_len),
            "integer_digits=" + str(self.integer_digits),
            "decimal_places=" + str(self.decimal_places),
            "additional_format_len=" + str(self.additional_format_len),
        ])

    def __get_additional_format_len(self):
        if not is_float(self.data):
            return 0

        format_len = 0

        if float(self.data) < 0:
            # for minus character
            format_len += 1

        return format_len

    def __get_base_float_len(self):
        if any([self.integer_digits < 0, self.decimal_places < 0]):
            raise ValueError()

        float_len = self.integer_digits + self.decimal_places
        if self.decimal_places > 0:
            # for dot
            float_len += 1

        return float_len

    def __get_str_len(self):
        if self.typecode == Typecode.INT:
            return self.integer_digits + self.additional_format_len

        if self.typecode == Typecode.FLOAT:
            return self.__get_base_float_len() + self.additional_format_len

        return get_text_len(self.data)

    def __set_data(self, data, replace_tabs_with_spaces, tab_length):
        self.__data = convert_value(data)

        if replace_tabs_with_spaces:
            try:
                self.__data = self.__data.replace("\t", " " * tab_length)
            except AttributeError:
                pass


class ColumnDataProperty(DataPeropertyInterface):
    __slots__ = (
        "__typecode_bitmap",
        "__str_len",
        "__minmax_integer_digits",
        "__minmax_decimal_places",
        "__minmax_additional_format_len",
    )

    @property
    def align(self):
        return align_getter.get_align_from_typecode(self.typecode)

    @property
    def decimal_places(self):
        try:
            avg = self.minmax_decimal_places.mean()
        except TypeError:
            return float("nan")

        if is_nan(avg):
            return float("nan")

        return int(math.ceil(avg))

    @property
    def typecode(self):
        return Typecode.get_typecode_from_bitmap(self.__typecode_bitmap)

    @property
    def padding_len(self):
        return self.__str_len

    @property
    def minmax_integer_digits(self):
        return self.__minmax_integer_digits

    @property
    def minmax_decimal_places(self):
        return self.__minmax_decimal_places

    @property
    def minmax_additional_format_len(self):
        return self.__minmax_additional_format_len

    def __init__(self, min_padding_len=0):
        self.__typecode_bitmap = Typecode.NONE
        self.__str_len = min_padding_len
        self.__minmax_integer_digits = MinMaxContainer()
        self.__minmax_decimal_places = MinMaxContainer()
        self.__minmax_additional_format_len = MinMaxContainer()

    def __repr__(self):
        return ", ".join([
            "typename=" + Typecode.get_typename(self.typecode),
            "align=" + str(self.align),
            "padding_len=" + str(self.padding_len),
            "integer_digits=(%s)" % (str(self.minmax_integer_digits)),
            "decimal_places=(%s)" % (str(self.minmax_decimal_places)),
            "additional_format_len=(%s)" % (
                str(self.minmax_additional_format_len)),
        ])

    def update_header(self, dataprop):
        self.__update(dataprop)

    def update_body(self, dataprop):
        self.__typecode_bitmap |= dataprop.typecode
        self.__update(dataprop)

    def __update(self, dataprop):
        self.__str_len = max(self.__str_len, dataprop.str_len)

        if dataprop.typecode in (Typecode.FLOAT, Typecode.INT):
            self.__minmax_integer_digits.update(dataprop.integer_digits)

        if dataprop.typecode == Typecode.FLOAT:
            self.__minmax_decimal_places.update(dataprop.decimal_places)

        self.__minmax_additional_format_len.update(
            dataprop.additional_format_len)
