# encoding: utf-8

'''
@author: Tsuyoshi Hombashi
'''

from __future__ import absolute_import
import abc
import math

import six

from ._align import Align
from ._container import MinMaxContainer
from ._typecode import Typecode


def is_integer(value):
    if isinstance(value, six.integer_types):
        return not isinstance(value, bool)

    try:
        int(value)
    except:
        return False

    if isinstance(value, float):
        return False

    return True


def is_hex(value):
    try:
        int(value, 16)
    except (TypeError, ValueError):
        return False

    return True


def is_float(value):
    if any([isinstance(value, float), value == float("inf")]):
        return True

    if isinstance(value, bool):
        return False

    try:
        work = float(value)
        if work == float("inf"):
            return False
    except:
        return False

    return True


def is_nan(value):
    return value != value


def is_empty_string(value):
    try:
        return len(value.strip()) == 0
    except AttributeError:
        return True


def is_not_empty_string(value):
    """
    空白文字(\0, \t, \n)を除いた文字数が0より大きければTrueを返す
    """

    try:
        return len(value.strip()) > 0
    except AttributeError:
        return False


def _is_list(value):
    return isinstance(value, list)


def _is_tuple(value):
    return isinstance(value, tuple)


def is_list_or_tuple(value):
    return any([_is_list(value), _is_tuple(value)])


def is_empty_list_or_tuple(value):
    return value is None or (is_list_or_tuple(value) and len(value) == 0)


def is_not_empty_list_or_tuple(value):
    return is_list_or_tuple(value) and len(value) > 0


def is_datetime(value):
    """
    :return: ``True``` if type of `value` is datetime.datetime.
    :rtype: bool
    """

    import datetime

    return value is not None and isinstance(value, datetime.datetime)


def get_integer_digit(value):
    abs_value = abs(float(value))

    if abs_value == 0:
        return 1

    return max(1, int(math.log10(abs_value) + 1.0))


def _get_decimal_places(value, integer_digits):
    from collections import namedtuple
    from six.moves import range

    float_digit_len = 0
    if is_integer(value):
        abs_value = abs(int(value))
    else:
        abs_value = abs(float(value))
        text_value = str(abs_value)
        float_text = 0
        if text_value.find(".") != -1:
            float_text = text_value.split(".")[1]
            float_digit_len = len(float_text)
        elif text_value.find("e-") != -1:
            float_text = text_value.split("e-")[1]
            float_digit_len = int(float_text) - 1

    Threshold = namedtuple("Threshold", "pow digit_len")
    upper_threshold = Threshold(pow=-2, digit_len=6)
    min_digit_len = 1

    treshold_list = [
        Threshold(upper_threshold.pow + i, upper_threshold.digit_len - i)
        for i, _
        in enumerate(range(upper_threshold.digit_len, min_digit_len - 1, -1))
    ]

    abs_digit = min_digit_len
    for treshold in treshold_list:
        if abs_value < math.pow(10, treshold.pow):
            abs_digit = treshold.digit_len
            break

    return min(abs_digit, float_digit_len)


def get_number_of_digit(value):
    try:
        integer_digits = get_integer_digit(value)
    except (ValueError, TypeError):
        integer_digits = float("nan")

    try:
        decimal_places = _get_decimal_places(value, integer_digits)
    except (ValueError, TypeError):
        decimal_places = float("nan")

    return (integer_digits, decimal_places)


def get_text_len(text):
    try:
        return len(str(text))
    except UnicodeEncodeError:
        return len(text)


def convert_value(value):
    if is_integer(value):
        value = int(value)
    elif is_float(value):
        value = float(value)

    return value


@six.add_metaclass(abc.ABCMeta)
class DataPeropertyInterface(object):

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


class DataProperty(DataPeropertyInterface):

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
        self.__align = PropertyExtractor.get_align_from_typecode(
            self.__typecode)

        integer_digits, decimal_places = get_number_of_digit(data)
        self.__integer_digits = integer_digits
        self.__decimal_places = decimal_places
        self.__additional_format_len = self.__get_additional_format_len(data)
        self.__str_len = self.__get_str_len()

    def __set_data(self, data, replace_tabs_with_spaces, tab_length):
        if replace_tabs_with_spaces:
            try:
                self.__data = data.replace("\t", " " * tab_length)
                return
            except AttributeError:
                pass

        self.__data = data

    def __repr__(self):
        return ", ".join([
            ("data=%" + self.format_str) % (convert_value(self.data)),
            "typename=" + Typecode.get_typename(self.typecode),
            "align=" + str(self.align),
            "str_len=" + str(self.str_len),
            "integer_digits=" + str(self.integer_digits),
            "decimal_places=" + str(self.decimal_places),
            "additional_format_len=" + str(self.additional_format_len),
        ])

    def __get_additional_format_len(self, data):
        if not is_float(data):
            return 0

        format_len = 0

        if float(data) < 0:
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


class ColumnDataPeroperty(DataPeropertyInterface):

    @property
    def align(self):
        return PropertyExtractor.get_align_from_typecode(self.typecode)

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

    def __init__(self):
        self.__typecode_bitmap = Typecode.NONE
        self.__str_len = 0
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


class PropertyExtractor:
    __typecode_align_table = {
        Typecode.STRING	: Align.LEFT,
        Typecode.INT	: Align.RIGHT,
        Typecode.FLOAT	: Align.RIGHT,
    }

    @classmethod
    def get_align_from_typecode(cls, typecode):
        return cls.__typecode_align_table.get(typecode, Align.LEFT)

    @classmethod
    def extract_data_property_matrix(cls, data_matrix):
        return [
            cls.__extract_data_property_list(data_list)
            for data_list in data_matrix
        ]

    @classmethod
    def extract_column_property_list(cls, header_list, data_matrix):
        data_prop_matrix = cls.extract_data_property_matrix(data_matrix)
        header_prop_list = cls.__extract_data_property_list(header_list)
        column_prop_list = []

        for col_idx, col_prop_list in enumerate(zip(*data_prop_matrix)):
            column_prop = ColumnDataPeroperty()

            if is_not_empty_list_or_tuple(header_prop_list):
                header_prop = header_prop_list[col_idx]
                column_prop.update_header(header_prop)

            for prop in col_prop_list:
                column_prop.update_body(prop)

            column_prop_list.append(column_prop)

        return column_prop_list

    @staticmethod
    def __extract_data_property_list(data_list):
        if is_empty_list_or_tuple(data_list):
            return []

        return [DataProperty(data) for data in data_list]
