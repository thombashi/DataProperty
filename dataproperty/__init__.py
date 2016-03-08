# encoding: utf-8

'''
@author: Tsuyoshi Hombashi
'''

import math

import six


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


def _get_base_float_len(integer_digits, decimal_places):
    if any([integer_digits < 0, decimal_places < 0]):
        raise ValueError()

    float_len = integer_digits + decimal_places
    if decimal_places > 0:
        # for dot
        float_len += 1

    return float_len


def _get_additional_format_len(data):
    if not is_float(data):
        return 0

    format_len = 0

    if float(data) < 0:
        # for minus character
        format_len += 1

    return format_len


class MinMaxContainer(object):

    @property
    def min_value(self):
        return self.__min_value

    @property
    def max_value(self):
        return self.__max_value

    def __init__(self):
        self.__min_value = None
        self.__max_value = None

    def diff(self):
        return self.max_value - self.min_value

    def average(self):
        return (self.max_value + self.min_value) * 0.5

    def update(self, value):
        if self.__min_value is None:
            self.__min_value = value
        else:
            self.__min_value = min(self.__min_value, value)

        if self.__max_value is None:
            self.__max_value = value
        else:
            self.__max_value = max(self.__max_value, value)


class Typecode:
    NONE = 0
    INT = 1 << 0
    FLOAT = 1 << 1
    STRING = 1 << 2

    __TYPENAME_TABLE = {
        NONE:   "NONE",
        INT:    "INT",
        FLOAT:  "FLOAT",
        STRING: "STRING",
    }

    @classmethod
    def get_typecode_from_bitmap(cls, typecode_bitmap):
        typecode_list = [cls.STRING, cls.FLOAT, cls.INT]

        for typecode in typecode_list:
            if typecode_bitmap & typecode:
                return typecode

        return cls.STRING

    @classmethod
    def get_typename(cls, typecode):
        return cls.__TYPENAME_TABLE.get(typecode)


class Align:

    class __AlignData:

        @property
        def align_code(self):
            return self.__align_code

        @property
        def align_string(self):
            return self.__align_string

        def __init__(self, code, string):
            self.__align_code = code
            self.__align_string = string

    AUTO = __AlignData(1 << 0, "auto")
    LEFT = __AlignData(1 << 1, "left")
    RIGHT = __AlignData(1 << 2, "right")
    CENTER = __AlignData(1 << 3, "center")


class DataPeroperty(object):

    @property
    def data(self):
        return self.__data

    @property
    def typecode(self):
        return self.__typecode

    @property
    def align(self):
        return self.__align

    @property
    def str_len(self):
        return self.__str_len

    @property
    def integer_digits(self):
        return self.__integer_digits

    @property
    def decimal_places(self):
        return self.__decimal_places

    @property
    def additional_format_len(self):
        return self.__additional_format_len

    @property
    def type_format(self):
        return self.__type_format

    def __init__(self, data):
        super(DataPeroperty, self).__init__()

        self.__data = data
        self.__typecode = self.__get_typecode(data)
        self.__align = PropertyExtractor.get_align_from_typecode(
            self.__typecode)

        integer_digits, decimal_places = get_number_of_digit(data)
        self.__integer_digits = integer_digits
        self.__decimal_places = decimal_places
        self.__additional_format_len = _get_additional_format_len(data)

        self.__type_format = self.__get_type_format(
            data, decimal_places)
        self.__str_len = self.__get_str_len()

    @staticmethod
    def __get_typecode(data):
        if data is None:
            return Typecode.NONE

        if is_integer(data):
            return Typecode.INT

        if is_float(data):
            return Typecode.FLOAT

        return Typecode.STRING

    @staticmethod
    def __get_type_format(value, decimal_places):
        if is_integer(value):
            return "d"
        if is_float(value):
            if is_nan(value):
                return "f"
            return ".%df" % (decimal_places)
        return "s"

    def __get_str_len(self):
        if self.typecode == Typecode.INT:
            return (
                self.integer_digits +
                _get_additional_format_len(self.data))

        if self.typecode == Typecode.FLOAT:
            return (
                _get_base_float_len(
                    self.integer_digits, self.decimal_places) +
                _get_additional_format_len(self.data))

        return get_text_len(self.data)


class ColumnDataPeroperty(object):

    @property
    def typecode(self):
        return Typecode.get_typecode_from_bitmap(self.typecode_bitmap)

    @property
    def align(self):
        return PropertyExtractor.get_align_from_typecode(self.typecode)

    @property
    def padding_len(self):
        return self.__str_len

    @property
    def decimal_places(self):
        try:
            avg = self.minmax_decimal_places.average()
        except TypeError:
            return float("nan")

        if is_nan(avg):
            return float("nan")

        return int(math.ceil(avg))

    def __init__(self):
        self.typecode_bitmap = Typecode.NONE
        self.__str_len = 0
        self.type_format = None
        self.minmax_integer_digits = MinMaxContainer()
        self.minmax_decimal_places = MinMaxContainer()
        self.minmax_additional_format_len = MinMaxContainer()

    def update_padding_len(self, padding_len):
        self.__str_len = max(self.__str_len, padding_len)

    def update_header(self, prop):
        self.update_padding_len(prop.str_len)

        if prop.typecode in (Typecode.FLOAT, Typecode.INT):
            self.minmax_integer_digits.update(prop.integer_digits)

        if prop.typecode == Typecode.FLOAT:
            self.minmax_decimal_places.update(prop.decimal_places)

        self.minmax_additional_format_len.update(prop.additional_format_len)

    def update_body(self, prop):
        self.typecode_bitmap |= prop.typecode
        self.update_header(prop)


class PropertyExtractor:
    __dict_ValueType_Align = {
        Typecode.STRING	: Align.LEFT,
        Typecode.INT	: Align.RIGHT,
        Typecode.FLOAT	: Align.RIGHT,
    }

    @classmethod
    def get_align_from_typecode(cls, typecode):
        return cls.__dict_ValueType_Align.get(typecode, Align.LEFT)

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

            decimal_places = 0
            if column_prop.typecode == Typecode.FLOAT:
                decimal_places = column_prop.decimal_places

                float_len = (
                    _get_base_float_len(
                        column_prop.minmax_integer_digits.max_value,
                        decimal_places) +
                    column_prop.minmax_additional_format_len.max_value
                )
                column_prop.update_padding_len(float_len)

            column_prop.type_format = cls.__get_column_type_format(
                column_prop.typecode, decimal_places)

            column_prop_list.append(column_prop)

        return column_prop_list

    @staticmethod
    def __extract_data_property_list(data_list):
        if is_empty_list_or_tuple(data_list):
            return []

        return [DataPeroperty(data) for data in data_list]

    @staticmethod
    def __get_column_type_format(typecode, decimal_places):
        if typecode == Typecode.INT:
            return "d"
        if typecode == Typecode.FLOAT:
            if is_nan(decimal_places):
                return "f"
            return ".%df" % (decimal_places)
        return "s"
