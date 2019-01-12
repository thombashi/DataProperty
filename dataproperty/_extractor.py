# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

from __future__ import absolute_import, unicode_literals

import copy
import enum
import multiprocessing
from collections import Counter

from six import text_type
from six.moves import zip
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
    StrictLevel,
    String,
    is_empty_sequence,
)

from ._column import ColumnDataProperty
from ._common import NOT_STRICT_TYPE_MAP, DefaultValue
from ._converter import DataPropertyConverter
from ._dataproperty import DataProperty
from ._formatter import Format
from ._line_break import LineBreakHandling
from .logger import logger


@enum.unique
class MatrixFormatting(enum.Enum):
    # raise exception if the matrix is not properly formatted
    EXCEPTION = 1 << 1

    # trim to the minimum size column
    TRIM = 1 << 2

    # Append None values to columns so that it is the same as the maximum
    # column size.
    FILL_NONE = 1 << 3

    HEADER_ALIGNED = 1 << 4


class DataPropertyExtractor(object):
    """
    .. py:attribute:: quoting_flags

        Configurations to add double quote to for each items in a matrix,
        where |Typecode| of table-value is |True| in the ``quote_flag_table``
        mapping table. ``quote_flag_table`` should be a dictionary.
        And is ``{ Typecode : bool }``. Defaults to:

        .. code-block:: json
            :caption: The default values

            {
                Typecode.BOOL: False,
                Typecode.DATETIME: False,
                Typecode.DICTIONARY: False,
                Typecode.INFINITY: False,
                Typecode.INTEGER: False,
                Typecode.IP_ADDRESS: False,
                Typecode.LIST: False,
                Typecode.NAN: False,
                Typecode.NULL_STRING: False,
                Typecode.NONE: False,
                Typecode.REAL_NUMBER: False,
                Typecode.STRING: False,
            }
    """

    @property
    def header_list(self):
        return self.__header_list

    @header_list.setter
    def header_list(self, value):
        if self.__header_list == value:
            return

        self.__header_list = value
        self.__clear_cache()

    @property
    def default_type_hint(self):
        return self.__default_type_hint

    @default_type_hint.setter
    def default_type_hint(self, value):
        if self.__default_type_hint == value:
            return

        self.__default_type_hint = value
        self.__clear_cache()

    @property
    def column_type_hint_list(self):
        return self.__col_type_hint_list

    @column_type_hint_list.setter
    def column_type_hint_list(self, value):
        if self.__col_type_hint_list == value:
            return

        if value:
            for type_hint in value:
                if type_hint not in (
                    Bool,
                    DateTime,
                    Dictionary,
                    Infinity,
                    Integer,
                    IpAddress,
                    List,
                    Nan,
                    NoneType,
                    RealNumber,
                    String,
                    NullString,
                    None,
                ):
                    raise ValueError("invalid type hint: {}".format(type(type_hint)))

        self.__col_type_hint_list = value
        self.__clear_cache()

    @property
    def line_break_handling(self):
        return self.__line_break_handling

    @line_break_handling.setter
    def line_break_handling(self, value):
        if self.__line_break_handling == value:
            return

        self.__line_break_handling = value
        self.__update_dp_converter()

    @property
    def is_formatting_float(self):
        return self.__is_formatting_float

    @is_formatting_float.setter
    def is_formatting_float(self, value):
        self.__is_formatting_float = value

    @property
    def is_escape_html_tag(self):
        return self.__is_escape_html_tag

    @is_escape_html_tag.setter
    def is_escape_html_tag(self, value):
        if self.__is_escape_html_tag == value:
            return

        self.__is_escape_html_tag = value
        self.__update_dp_converter()

    @property
    def strip_str_header(self):
        return self.__strip_str_header

    @strip_str_header.setter
    def strip_str_header(self, value):
        if self.__strip_str_header == value:
            return

        self.__strip_str_header = value
        self.__clear_cache()

    @property
    def strip_str_value(self):
        return self.__strip_str_value

    @strip_str_value.setter
    def strip_str_value(self, value):
        if self.__strip_str_value == value:
            return

        self.__strip_str_value = value
        self.__clear_cache()

    @property
    def min_column_width(self):
        return self.__min_col_ascii_char_width

    @min_column_width.setter
    def min_column_width(self, value):
        if self.__min_col_ascii_char_width == value:
            return

        self.__min_col_ascii_char_width = value
        self.__clear_cache()

    @property
    def format_flags_list(self):
        return self.__format_flags_list

    @format_flags_list.setter
    def format_flags_list(self, value):
        if self.__format_flags_list == value:
            return

        self.__format_flags_list = value
        self.__clear_cache()

    @property
    def float_type(self):
        return self.__float_type

    @float_type.setter
    def float_type(self, value):
        if self.__float_type == value:
            return

        self.__float_type = value
        self.__clear_cache()

    @property
    def datetime_format_str(self):
        return self.__datetime_format_str

    @datetime_format_str.setter
    def datetime_format_str(self, value):
        if self.__datetime_format_str == value:
            return

        self.__datetime_format_str = value
        self.__clear_cache()

    @property
    def strict_type_map(self):
        return self.__strict_type_map

    @strict_type_map.setter
    def strict_type_map(self, value):
        if self.__strict_type_map == value:
            return

        self.__strict_type_map = value
        self.__clear_cache()

    @property
    def east_asian_ambiguous_width(self):
        return self.__east_asian_ambiguous_width

    @east_asian_ambiguous_width.setter
    def east_asian_ambiguous_width(self, value):
        if self.__east_asian_ambiguous_width == value:
            return

        self.__east_asian_ambiguous_width = value
        self.__clear_cache()

    @property
    def type_value_map(self):
        return self.__type_value_map

    @type_value_map.setter
    def type_value_map(self, value):
        if self.__type_value_map == value:
            return

        self.__type_value_map = value
        self.__clear_cache()

    @property
    def const_value_map(self):
        return self.__const_value_map

    @const_value_map.setter
    def const_value_map(self, value):
        if self.__const_value_map == value:
            return

        self.__const_value_map = value
        self.__clear_cache()

    @property
    def quoting_flags(self):
        return self.__quoting_flags

    @quoting_flags.setter
    def quoting_flags(self, value):
        if self.__quoting_flags == value:
            return

        self.__quoting_flags = value
        self.__clear_cache()

    @property
    def datetime_formatter(self):
        return self.__datetime_formatter

    @datetime_formatter.setter
    def datetime_formatter(self, value):
        if self.__datetime_formatter == value:
            return

        self.__datetime_formatter = value
        self.__clear_cache()

    @property
    def matrix_formatting(self):
        return self.__matrix_formatting

    @matrix_formatting.setter
    def matrix_formatting(self, value):
        if self.__matrix_formatting == value:
            return

        self.__matrix_formatting = value
        self.__clear_cache()

    def __init__(self):
        self.max_workers = multiprocessing.cpu_count()

        self.__header_list = []
        self.__default_type_hint = None
        self.__col_type_hint_list = None

        self.__strip_str_header = None
        self.__strip_str_value = None
        self.__is_formatting_float = True
        self.__line_break_handling = LineBreakHandling.NOP
        self.__is_escape_html_tag = False
        self.__min_col_ascii_char_width = 0
        self.__format_flags_list = []
        self.__float_type = None
        self.__datetime_format_str = DefaultValue.DATETIME_FORMAT
        self.__strict_type_map = copy.deepcopy(DefaultValue.STRICT_LEVEL_MAP)
        self.__east_asian_ambiguous_width = 1

        self.__type_value_map = copy.deepcopy(DefaultValue.TYPE_VALUE_MAP)
        self.__const_value_map = copy.deepcopy(DefaultValue.CONST_VALUE_MAP)
        self.__quoting_flags = copy.deepcopy(DefaultValue.QUOTING_FLAGS)
        self.__datetime_formatter = None
        self.__matrix_formatting = MatrixFormatting.TRIM

        self.__clear_cache()

    def __clear_cache(self):
        self.__update_dp_converter()
        self.__dp_cache_zero = self.__to_dp_raw(0)
        self.__dp_cache_one = self.__to_dp_raw(1)
        self.__dp_cache_true = self.__to_dp_raw(True)
        self.__dp_cache_false = self.__to_dp_raw(False)
        self.__dp_cache_map = {None: self.__to_dp_raw(None), "": self.__to_dp_raw("")}

    def to_dp(self, value):
        self.__update_dp_converter()

        return self.__to_dp(value, strip_str=self.strip_str_value)

    def to_dp_list(self, value_list):
        if is_empty_sequence(value_list):
            return []

        self.__update_dp_converter()

        return self._to_dp_list(value_list, strip_str=self.strip_str_value)

    def to_column_dp_list(self, value_dp_matrix, previous_column_dp_list=None):
        logger.debug(
            "prev_col_count={}, mismatch_process={}".format(
                len(previous_column_dp_list) if previous_column_dp_list else None,
                self.matrix_formatting,
            )
        )

        col_dp_list = self.__get_col_dp_list_base()

        logger.debug("converting to column dataproperty:")
        for col_idx, value_dp_list in enumerate(zip(*value_dp_matrix)):
            try:
                col_dp_list[col_idx]
            except IndexError:
                col_dp_list.append(
                    ColumnDataProperty(
                        column_index=col_idx,
                        min_width=self.min_column_width,
                        format_flags=self.__get_format_flags(col_idx),
                        is_formatting_float=self.is_formatting_float,
                        datetime_format_str=self.datetime_format_str,
                        east_asian_ambiguous_width=self.east_asian_ambiguous_width,
                    )
                )

            col_dp = col_dp_list[col_idx]
            col_dp.begin_update()

            try:
                col_dp.merge(previous_column_dp_list[col_idx])
            except (TypeError, IndexError):
                pass

            for value_dp in value_dp_list:
                col_dp.update_body(value_dp)

            col_dp.end_update()

            logger.debug("  {:s}".format(text_type(col_dp)))

        return col_dp_list

    def to_dp_matrix(self, value_matrix):
        self.__update_dp_converter()
        logger.debug("max_workers = {}".format(self.max_workers))

        value_matrix = self.__strip_data_matrix(value_matrix)

        if self.__is_dp_matrix(value_matrix):
            logger.debug("already a dataproperty matrix")
            return value_matrix

        if not self.max_workers:
            self.max_workers = multiprocessing.cpu_count()

        if self.max_workers <= 1:
            return self.__to_dp_matrix_st(value_matrix)

        return self.__to_dp_matrix_mt(value_matrix)

    def to_header_dp_list(self):
        self.__update_dp_converter()

        return self._to_dp_list(
            self.header_list,
            type_hint=String,
            strip_str=self.strip_str_header,
            strict_type_map=NOT_STRICT_TYPE_MAP,
        )

    @staticmethod
    def __is_dp_matrix(value):
        if not value:
            return False

        try:
            return isinstance(value[0][0], DataProperty)
        except (TypeError, IndexError):
            return False

    def __get_col_type_hint(self, col_idx):
        try:
            return self.column_type_hint_list[col_idx]
        except (TypeError, IndexError):
            return self.default_type_hint

    def __get_format_flags(self, col_idx):
        try:
            return self.format_flags_list[col_idx]
        except (TypeError, IndexError):
            return Format.NONE

    def __to_dp(self, data, type_hint=None, strip_str=None, strict_type_map=None):
        try:
            if data in self.__dp_cache_map:
                return self.__dp_cache_map.get(data)
        except TypeError:
            # unhashable type
            pass

        if data == 0:
            if text_type(data) != "False":
                return self.__dp_cache_zero

            return self.__dp_cache_false
        if data == 1:
            if text_type(data) != "True":
                return self.__dp_cache_one

            return self.__dp_cache_true

        return self.__to_dp_raw(
            data, type_hint=type_hint, strip_str=strip_str, strict_type_map=strict_type_map
        )

    def __to_dp_raw(self, data, type_hint=None, strip_str=None, strict_type_map=None):
        value_dp = DataProperty(
            data,
            type_hint=(type_hint if type_hint is not None else self.default_type_hint),
            line_break_handling=self.line_break_handling,
            strip_str=strip_str,
            float_type=self.float_type,
            datetime_format_str=self.datetime_format_str,
            strict_type_map=(strict_type_map if type_hint is not None else self.strict_type_map),
            east_asian_ambiguous_width=self.east_asian_ambiguous_width,
        )

        return self.__dp_converter.convert(value_dp)

    def __to_dp_matrix_st(self, value_matrix):
        return list(
            zip(
                *[
                    _to_dp_list_helper(
                        self,
                        col_idx,
                        data_list,
                        self.__get_col_type_hint(col_idx),
                        self.strip_str_value,
                    )[1]
                    for col_idx, data_list in enumerate(zip(*value_matrix))
                ]
            )
        )

    def __to_dp_matrix_mt(self, value_matrix):
        from concurrent import futures

        col_data_map = {}

        try:
            with futures.ProcessPoolExecutor(self.max_workers) as executor:
                future_list = [
                    executor.submit(
                        _to_dp_list_helper,
                        self,
                        col_idx,
                        data_list,
                        self.__get_col_type_hint(col_idx),
                        self.strip_str_value,
                    )
                    for col_idx, data_list in enumerate(zip(*value_matrix))
                ]

                for future in futures.as_completed(future_list):
                    col_idx, value_dp_list = future.result()
                    col_data_map[col_idx] = value_dp_list
        finally:
            logger.debug("shutdown ProcessPoolExecutor")
            executor.shutdown()

        return list(zip(*[col_data_map[col_idx] for col_idx in sorted(col_data_map)]))

    def _to_dp_list(self, data_list, type_hint=None, strip_str=None, strict_type_map=None):
        if is_empty_sequence(data_list):
            return []

        type_counter = Counter()

        dp_list = []
        for data in data_list:
            expect_type_hist = type_hint
            if type_hint is None:
                try:
                    expect_type_hist, _count = type_counter.most_common(1)[0]
                    if not expect_type_hist(data, strict_level=StrictLevel.MAX).is_type():
                        expect_type_hist = None
                except IndexError:
                    pass

            dataprop = self.__to_dp(
                data=data,
                type_hint=expect_type_hist,
                strip_str=strip_str,
                strict_type_map=strict_type_map,
            )
            type_counter[dataprop.type_class] += 1

            dp_list.append(dataprop)

        return dp_list

    def __strip_data_matrix(self, data_matrix):
        header_col_size = len(self.header_list) if self.header_list else 0
        try:
            col_size_list = [len(data_list) for data_list in data_matrix]
        except TypeError:
            return []

        if self.header_list:
            min_col_size = min([header_col_size] + col_size_list)
            max_col_size = max([header_col_size] + col_size_list)
        elif col_size_list:
            min_col_size = min(col_size_list)
            max_col_size = max(col_size_list)
        else:
            min_col_size = 0
            max_col_size = 0

        if self.matrix_formatting == MatrixFormatting.EXCEPTION:
            if min_col_size != max_col_size:
                raise ValueError(
                    "nonuniform column size: min={}, max={}".format(min_col_size, max_col_size)
                )

            return data_matrix

        if self.matrix_formatting == MatrixFormatting.HEADER_ALIGNED:
            if header_col_size > 0:
                format_col_size = header_col_size
            else:
                format_col_size = max_col_size
        elif self.matrix_formatting == MatrixFormatting.TRIM:
            format_col_size = min_col_size
        elif self.matrix_formatting == MatrixFormatting.FILL_NONE:
            format_col_size = max_col_size
        else:
            raise ValueError("unknown matrix formatting: {}".format(self.matrix_formatting))

        return [
            list(data_matrix[row_idx][:format_col_size]) + [None] * (format_col_size - col_size)
            for row_idx, col_size in enumerate(col_size_list)
        ]

    def __get_col_dp_list_base(self):
        header_dp_list = self.to_header_dp_list()
        col_dp_list = []

        for col_idx, header_dp in enumerate(header_dp_list):
            col_dp = ColumnDataProperty(
                column_index=col_idx,
                min_width=self.min_column_width,
                format_flags=self.__get_format_flags(col_idx),
                is_formatting_float=self.is_formatting_float,
                datetime_format_str=self.datetime_format_str,
                east_asian_ambiguous_width=self.east_asian_ambiguous_width,
            )
            col_dp.update_header(header_dp)
            col_dp_list.append(col_dp)

        return col_dp_list

    def __update_dp_converter(self):
        self.__dp_converter = DataPropertyConverter(
            type_value_map=self.type_value_map,
            const_value_map=self.const_value_map,
            quoting_flags=self.quoting_flags,
            line_break_handling=self.line_break_handling,
            is_escape_html_tag=self.is_escape_html_tag,
            datetime_formatter=self.datetime_formatter,
            datetime_format_str=self.datetime_format_str,
            float_type=self.float_type,
            strict_type_map=self.strict_type_map,
        )


def _to_dp_list_helper(extractor, col_idx, data_list, type_hint, strip_str):
    return (col_idx, extractor._to_dp_list(data_list, type_hint=type_hint, strip_str=strip_str))
