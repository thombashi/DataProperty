# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <gogogo.vm@gmail.com>
"""

from __future__ import absolute_import
import math


def is_integer(value):
    """
    .. warning::

        This function will be deleted in the future.
        Use IntegerTypeChecker class instead of this function.
    """

    from .type import IntegerTypeChecker

    return IntegerTypeChecker(value).is_type()


def is_hex(value):
    try:
        int(value, 16)
    except (TypeError, ValueError):
        return False

    return True


def is_float(value):
    """
    .. warning::

        This function will be deleted in the future.
        Use FloatTypeChecker class instead of this function.
    """

    from .type import FloatTypeChecker

    return FloatTypeChecker(value).is_type()


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


def is_empty_sequence(value):
    try:
        return value is None or len(value) == 0
    except TypeError:
        return False


def is_not_empty_sequence(value):
    try:
        return len(value) > 0
    except TypeError:
        return False


def is_empty_list_or_tuple(value):
    """
    .. warning::

        This function will be deleted in the future.
        Use is_not_empty_sequence function instead of this.
    """

    return value is None or (is_list_or_tuple(value) and len(value) == 0)


def is_not_empty_list_or_tuple(value):
    """
    .. warning::

        This function will be deleted in the future.
        Use is_not_empty_sequence function instead of this.
    """

    return is_list_or_tuple(value) and len(value) > 0


def is_datetime(value):
    """
    :return: ``True``` if type of `value` is datetime.datetime.
    :rtype: bool

    .. warning::

        This function will be deleted in the future.
        Use IntegerTypeChecker class instead of this function.
    """

    import datetime

    return value is not None and isinstance(value, datetime.datetime)


def get_integer_digit(value):
    from .type import FloatTypeChecker

    abs_value = abs(float(value))

    if not FloatTypeChecker(value).is_type():
        # bool type value reaches this line
        raise TypeError("invalid type '{:s}".format(type(value)))

    if abs_value == 0:
        return 1

    return max(1, int(math.log10(abs_value) + 1.0))


def _get_decimal_places(value, integer_digits):
    from collections import namedtuple
    from six.moves import range
    from .type import IntegerTypeChecker

    float_digit_len = 0
    if IntegerTypeChecker(value).is_type():
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
    nan = float("nan")

    try:
        integer_digits = get_integer_digit(value)
    except (ValueError, TypeError, OverflowError):
        return (nan, nan)

    try:
        decimal_places = _get_decimal_places(value, integer_digits)
    except (ValueError, TypeError):
        decimal_places = nan

    return (integer_digits, decimal_places)


def get_text_len(text):
    try:
        return len(str(text))
    except UnicodeEncodeError:
        return len(text)


def strict_strtobool(value):
    from distutils.util import strtobool

    if isinstance(value, bool):
        return value

    try:
        lower_text = value.lower()
    except AttributeError:
        raise ValueError("invalid value '{:s}'".format(str(value)))

    binary_value = strtobool(lower_text)
    if lower_text not in ["true", "false"]:
        raise ValueError("invalid value '{:s}'".format(str(value)))

    return bool(binary_value)
