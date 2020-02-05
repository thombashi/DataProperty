# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

from __future__ import absolute_import, unicode_literals

import decimal
import math
import re
from collections import namedtuple
from decimal import Decimal

from mbstrdecoder import MultiByteStrDecoder
from six import text_type
from six.moves import range
from typepy import Integer, RealNumber, TypeConversionError


decimal.setcontext(decimal.Context(prec=60, rounding=decimal.ROUND_HALF_DOWN))

_ansi_escape = re.compile(r"(\x9b|\x1b\[)[0-?]*[ -\/]*[@-~]", re.IGNORECASE)


def get_integer_digit(value):
    float_type = RealNumber(value)

    try:
        abs_value = abs(float_type.convert())
    except TypeConversionError:
        try:
            abs_value = abs(Integer(value).convert())
        except TypeConversionError:
            raise ValueError(
                "the value must be a number: value='{}' type='{}'".format(value, type(value))
            )

        return len(text_type(abs_value))

    if abs_value.is_zero():
        return 1

    try:
        return len(text_type(abs_value.quantize(Decimal("1."), rounding=decimal.ROUND_DOWN)))
    except decimal.InvalidOperation:
        return len(text_type(abs_value))


class DigitCalculator(object):
    Threshold = namedtuple("Threshold", "pow digit_len")

    def __init__(self):
        upper_threshold = self.Threshold(pow=-2, digit_len=6)

        self.__min_digit_len = 1
        self.__thresholds = [
            self.Threshold(upper_threshold.pow + i, upper_threshold.digit_len - i)
            for i, _ in enumerate(range(upper_threshold.digit_len, self.__min_digit_len - 1, -1))
        ]

    def get_decimal_places(self, value):
        from typepy import Integer

        int_type = Integer(value)

        float_digit_len = 0
        if int_type.is_type():
            abs_value = abs(int_type.convert())
        else:
            abs_value = abs(float(value))
            text_value = text_type(abs_value)
            float_text = 0
            if text_value.find(".") != -1:
                float_text = text_value.split(".")[1]
                float_digit_len = len(float_text)
            elif text_value.find("e-") != -1:
                float_text = text_value.split("e-")[1]
                float_digit_len = int(float_text) - 1

        abs_digit = self.__min_digit_len
        for threshold in self.__thresholds:
            if abs_value < math.pow(10, threshold.pow):
                abs_digit = threshold.digit_len
                break

        return min(abs_digit, float_digit_len)


_digit_calculator = DigitCalculator()


def get_number_of_digit(value):
    try:
        integer_digits = get_integer_digit(value)
    except (ValueError, TypeError, OverflowError):
        return (None, None)

    try:
        decimal_places = _digit_calculator.get_decimal_places(value)
    except (ValueError, TypeError):
        decimal_places = None

    return (integer_digits, decimal_places)


def is_multibyte_str(text):
    from typepy import StrictLevel, String

    if not String(text, strict_level=StrictLevel.MIN).is_type():
        return False

    try:
        unicode_text = MultiByteStrDecoder(text).unicode_str
    except ValueError:
        return False

    try:
        unicode_text.encode("ascii")
    except UnicodeEncodeError:
        return True

    return False


def _validate_eaaw(east_asian_ambiguous_width):
    if east_asian_ambiguous_width in (1, 2):
        return

    raise ValueError(
        "invalid east_asian_ambiguous_width: expected=1 or 2, actual={}".format(
            east_asian_ambiguous_width
        )
    )


def strip_ansi_escape(unicode_str):
    return _ansi_escape.sub("", unicode_str)


def calc_ascii_char_width(unicode_str, east_asian_ambiguous_width=1):
    import unicodedata

    width = 0
    for char in unicode_str:
        char_width = unicodedata.east_asian_width(char)
        if char_width in "WF":
            width += 2
        elif char_width == "A":
            _validate_eaaw(east_asian_ambiguous_width)
            width += east_asian_ambiguous_width
        else:
            width += 1

    return width
