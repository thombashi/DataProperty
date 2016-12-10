# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <gogogo.vm@gmail.com>
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals
import abc
import re

from mbstrdecoder import MultiByteStrDecoder

from ._error import TypeConversionError


class ValueConverterInterface(object):

    @abc.abstractmethod
    def convert(self):  # pragma: no cover
        pass

    @abc.abstractmethod
    def try_convert(self):  # pragma: no cover
        pass


class ValueConverter(ValueConverterInterface):
    __slots__ = ("_value")

    def __init__(self, value):
        self._value = value

    def __repr__(self):
        try:
            string = str(self.convert())
        except TypeConversionError:
            string = "[ValueConverter ERROR] failed to convert"

        return string

    def try_convert(self):
        try:
            return self.convert()
        except TypeConversionError:
            return None


class NopConverter(ValueConverter):

    def convert(self):
        return self._value


class StringConverter(ValueConverter):

    def convert(self):
        return MultiByteStrDecoder(self._value).unicode_str


class IntegerConverter(ValueConverter):

    def convert(self):
        try:
            return int(self._value)
        except (TypeError, ValueError, OverflowError):
            try:
                raise TypeConversionError(
                    "failed to convert: {}".format(self._value))
            except (UnicodeEncodeError, UnicodeDecodeError):
                raise TypeConversionError("failed to convert to integer")


class FloatConverter(ValueConverter):

    def convert(self):
        import decimal

        if isinstance(self._value, float):
            return decimal.Decimal(str(self._value))

        try:
            return decimal.Decimal(self._value)
        except (TypeError, ValueError, decimal.InvalidOperation):
            try:
                raise TypeConversionError(
                    "failed to convert: {}".format(self._value))
            except (UnicodeEncodeError, UnicodeDecodeError):
                raise TypeConversionError("failed to convert to float")


class BoolConverter(ValueConverter):

    def convert(self):
        try:
            return self.__strict_strtobool(self._value)
        except ValueError:
            try:
                raise TypeConversionError(
                    "failed to convert: {}".format(self._value))
            except (UnicodeEncodeError, UnicodeDecodeError):
                raise TypeConversionError("failed to convert to bool")

    @staticmethod
    def __strict_strtobool(value):
        from distutils.util import strtobool

        if isinstance(value, bool):
            return value

        try:
            lower_text = value.lower()
        except AttributeError:
            raise ValueError("invalid value '{}'".format(str(value)))

        binary_value = strtobool(lower_text)
        if lower_text not in ["true", "false"]:
            raise ValueError("invalid value '{}'".format(str(value)))

        return bool(binary_value)


class DateTimeConverter(ValueConverter):

    __DAYS_TO_SECONDS_COEF = 60 ** 2 * 24
    __MICROSECONDS_TO_SECONDS_COEF = 1000 ** 2
    __COMMON_DST_TIMEZONE_TABLE = {
        -36000: "America/Adak",  # -1000
        -32400: "US/Alaska",  # -0900
        -28800: "US/Pacific",  # -0800
        -25200: "US/Mountain",  # -0700
        -21600: "US/Central",  # -0600
        -18000: "US/Eastern",  # -0500
        -14400: "Canada/Atlantic",  # -0400
        -12600: "America/St_Johns",  # -0330
        -10800: "America/Miquelon",  # -0300
        7200: "Africa/Tripoli",  # 0200
    }

    __RE_VERSION_STR = re.compile("\d+\.\d+\.\d")

    def __init__(self, value):
        super(DateTimeConverter, self).__init__(value)

        self.__datetime = None

    def convert(self):
        import datetime
        import dateutil.parser
        import pytz

        if isinstance(self._value, datetime.datetime):
            self.__datetime = self._value
            return self.__datetime

        self.__validate_datetime_string()

        try:
            self.__datetime = dateutil.parser.parse(self._value)
        except (AttributeError, ValueError, OverflowError):
            try:
                raise TypeConversionError(
                    "failed to parse as a datetime: {}".format(self._value))
            except (UnicodeEncodeError, UnicodeDecodeError):
                raise TypeConversionError("failed to parse as a datetime")

        try:
            dst_timezone_name = self.__get_dst_timezone_name(
                self.__get_timedelta_sec())
        except (AttributeError, KeyError):
            return self.__datetime

        pytz_timezone = pytz.timezone(dst_timezone_name)
        self.__datetime = self.__datetime.replace(tzinfo=None)
        self.__datetime = pytz_timezone.localize(self.__datetime)

        return self.__datetime

    def __get_timedelta_sec(self):
        dt = self.__datetime.utcoffset()

        return int(
            (
                dt.days *
                self.__DAYS_TO_SECONDS_COEF +
                float(dt.seconds)
            ) +
            dt.microseconds / self.__MICROSECONDS_TO_SECONDS_COEF
        )

    def __get_dst_timezone_name(self, offset):
        return self.__COMMON_DST_TIMEZONE_TABLE[offset]

    def __validate_datetime_string(self):
        """
        This will require validating version string (such as "3.3.5").
        A version string could be converted to a datetime value if this
        validation is not executed.
        """

        try:
            if self.__RE_VERSION_STR.search(self._value) is not None:
                raise TypeConversionError(
                    "invalid datetime string: version string found " +
                    self._value)
        except TypeError:
            try:
                raise TypeConversionError(
                    "invalid datetime string: {}".format(self._value))
            except (UnicodeEncodeError, UnicodeDecodeError):
                raise TypeConversionError(
                    "invalid datetime string")


class DictionaryConverter(ValueConverter):

    def convert(self):
        try:
            return dict(self._value)
        except (TypeError, ValueError):
            try:
                raise TypeConversionError(
                    "failed to convert: {}".format(self._value))
            except (UnicodeEncodeError, UnicodeDecodeError):
                raise TypeConversionError("failed to convert to bool")
