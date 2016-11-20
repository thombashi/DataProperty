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
        Use IntegerType class instead of this function.
    """

    from ._type import IntegerType

    return IntegerType(value).is_type()


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
        Use FloatType class instead of this function.
    """

    from ._type import FloatType

    return FloatType(value).is_type()


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
    """
    .. warning::

        This function will be deleted in the future.
    """

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
        Use is_not_empty_sequence function instead of this function.
    """

    return value is None or (is_list_or_tuple(value) and len(value) == 0)


def is_not_empty_list_or_tuple(value):
    """
    .. warning::

        This function will be deleted in the future.
        Use is_not_empty_sequence function instead of this function.
    """

    return is_list_or_tuple(value) and len(value) > 0


def is_datetime(value):
    """
    :return: ``True``` if type of `value` is datetime.datetime.
    :rtype: bool

    .. warning::

        This function will be deleted in the future.
        Use DateTimeType class instead of this function.
    """

    from ._type import DateTimeType

    return DateTimeType(value).is_type()


def get_integer_digit(value):
    from ._type import FloatType

    abs_value = abs(float(value))

    if not FloatType(value).is_type():
        # bool type value reaches this line
        raise TypeError("invalid type '{:s}".format(type(value)))

    if abs_value == 0:
        return 1

    return max(1, int(math.log10(abs_value) + 1.0))


def _get_decimal_places(value, integer_digits):
    from collections import namedtuple
    from six.moves import range
    from ._type import IntegerType

    float_digit_len = 0
    if IntegerType(value).is_type():
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


_codec_list = (
    'ascii',
    'utf_8', 'utf_8_sig',
    'utf_7',
    'utf_16', 'utf_16_be', 'utf_16_le',
    'utf_32', 'utf_32_be', 'utf_32_le',

    'big5', 'big5hkscs',
    'cp037', 'cp424', 'cp437', 'cp500', 'cp720',
    'cp737', 'cp775', 'cp850', 'cp852', 'cp855',
    'cp856', 'cp857', 'cp858', 'cp860', 'cp861',
    'cp862', 'cp863', 'cp864', 'cp865', 'cp866',
    'cp869', 'cp874', 'cp875', 'cp932', 'cp949',
    'cp950', 'cp1006', 'cp1026', 'cp1140', 'cp1250',
    'cp1251', 'cp1252', 'cp1253', 'cp1254', 'cp1255',
    'cp1256', 'cp1257', 'cp1258',
    'euc_jp', 'euc_jis_2004', 'euc_jisx0213', 'euc_kr',
    'gb2312', 'gbk', 'gb18030',
    'hz',
    'iso2022_jp', 'iso2022_jp_1', 'iso2022_jp_2', 'iso2022_jp_2004',
    'iso2022_jp_3', 'iso2022_jp_ext', 'iso2022_kr',
    'latin_1',
    'iso8859_2', 'iso8859_3', 'iso8859_4', 'iso8859_5', 'iso8859_6',
    'iso8859_7', 'iso8859_8', 'iso8859_9', 'iso8859_10', 'iso8859_11',
    'iso8859_13', 'iso8859_14', 'iso8859_15', 'iso8859_16',
    'johab',
    'koi8_r', 'koi8_u',
    'mac_cyrillic', 'mac_greek', 'mac_iceland', 'mac_latin2', 'mac_roman', 'mac_turkish',
    'ptcp154',
    'shift_jis', 'shift_jis_2004', 'shift_jisx0213',
)


def to_unicode(value):
    for codec in _codec_list:
        try:
            return value.decode(codec)
        except UnicodeDecodeError:
            continue
        except UnicodeEncodeError:
            return value
        except AttributeError:
            return u"{}".format(value)

    raise ValueError("unknown codec: {}".format(value))


def is_multibyte_str(text):
    from ._type_checker import StringTypeChecker

    if not StringTypeChecker(text).is_type():
        return False

    unicode_text = to_unicode(text)

    try:
        unicode_text.encode("ascii")
    except UnicodeEncodeError:
        return True

    return False


def get_ascii_char_width(unicode_str):
    import unicodedata

    width = 0
    for c in unicode_str:
        char_width = unicodedata.east_asian_width(c)
        if char_width in u"WFA":
            width += 2
        else:
            width += 1

    return width
