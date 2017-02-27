# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <gogogo.vm@gmail.com>
"""

from __future__ import absolute_import
from __future__ import unicode_literals

import copy

from typepy import is_empty_sequence

from six.moves import zip

from ._common import (
    NOT_STRICT_TYPE_MAPPING,
    DefaultValue,
)
from ._dataproperty import (
    DataProperty,
    ColumnDataProperty,
)
from ._dataproperty_converter import DataPropertyConverter
from ._type import StringType


class MissmatchProcessing(object):
    EXCEPTION = 1 << 1
    TRIM = 1 << 2
    EXTEND = 1 << 3


class DataPropertyExtractor(object):
    """
    .. py:attribute:: quote_flag_mapping

        Configurations to add double quote to for each items in a matrix,
        where |Typecode| of table-value is |True| in the ``quote_flag_table``
        mapping table. ``quote_flag_table`` should be a dictionary.
        And is ``{ Typecode : bool }``. Defaults to:

        .. code-block:: json
            :caption: The default values

            {
                Typecode.NONE: False,
                Typecode.INTEGER: False,
                Typecode.FLOAT: False,
                Typecode.STRING: False,
                Typecode.NULL_STRING: False,
                Typecode.DATETIME: False,
                Typecode.FLOAT: False,
                Typecode.NAN: False,
                Typecode.BOOL: False,
            }
    """

    def __init__(self):
        self.header_list = []
        self.data_matrix = []
        self.default_type_hint = None
        self.col_type_hint_list = None

        self.strip_str = None
        self.min_padding_len = 0
        self.float_type = None
        self.datetime_format_str = DefaultValue.DATETIME_FORMAT
        self.strict_type_mapping = copy.deepcopy(
            DefaultValue.STRICT_TYPE_MAPPING)
        self.east_asian_ambiguous_width = 1

        self.type_value_mapping = copy.deepcopy(
            DefaultValue.TYPE_VALUE_MAPPING)
        self.const_value_mapping = copy.deepcopy(
            DefaultValue.CONST_VALUE_MAPPING)
        self.quote_flag_mapping = copy.deepcopy(
            DefaultValue.QUOTE_FLAG_MAPPING)
        self.datetime_formatter = None

        self.mismatch_processing = MissmatchProcessing.TRIM

    def to_dataproperty(self, data):
        self.__update_dp_converter()

        return self.__to_dataproperty(data)

    def to_dataproperty_list(self, data_list):
        if is_empty_sequence(data_list):
            return []

        self.__update_dp_converter()

        return [self.__to_dataproperty(data) for data in data_list]

    def to_col_dataproperty_list(self):
        col_dp_list = self.__get_col_dp_list_base()

        try:
            dp_matrix = self.to_dataproperty_matrix()
        except TypeError:
            return col_dp_list

        for col_idx, value_dp_list in enumerate(zip(*dp_matrix)):
            try:
                col_dp_list[col_idx]
            except IndexError:
                if self.mismatch_processing == MissmatchProcessing.EXCEPTION:
                    raise ValueError(
                        "column not found: col-size={}, col-index={}".format(
                            len(col_dp_list), col_idx))

                if any([
                    self.mismatch_processing == MissmatchProcessing.EXTEND,
                    all([
                        self.mismatch_processing == MissmatchProcessing.TRIM,
                        is_empty_sequence(self.header_list),
                    ])
                ]):
                    col_dp_list.append(ColumnDataProperty(
                        min_padding_len=self.min_padding_len,
                        datetime_format_str=self.datetime_format_str,
                        east_asian_ambiguous_width=self.east_asian_ambiguous_width
                    ))
                elif self.mismatch_processing == MissmatchProcessing.TRIM:
                    # ignore columns that longer than header column
                    continue

            for value_dp in value_dp_list:
                col_dp_list[col_idx].update_body(value_dp)

        return col_dp_list

    def to_dataproperty_matrix(self):
        self.__update_dp_converter()

        return list(zip(*[
            self.__to_dataproperty_list(
                data_list, type_hint=self.__get_col_type_hint(col_idx))
            for col_idx, data_list in enumerate(zip(*self.data_matrix))
        ]))

    def to_header_dataproperty_list(self):
        self.__update_dp_converter()

        return self.__to_dataproperty_list(
            self.header_list, type_hint=StringType,
            strict_type_mapping=NOT_STRICT_TYPE_MAPPING)

    def __get_col_type_hint(self, col_idx):
        try:
            return self.col_type_hint_list[col_idx]
        except (TypeError, IndexError):
            return self.default_type_hint

    def __to_dataproperty(
            self, data, type_hint=None, strict_type_mapping=None):
        dp = DataProperty(
            data,
            type_hint=(
                type_hint if type_hint is not None else self.default_type_hint),
            strip_str=self.strip_str,
            float_type=self.float_type,
            datetime_format_str=self.datetime_format_str,
            strict_type_mapping=(
                strict_type_mapping
                if type_hint is not None else self.strict_type_mapping),
            east_asian_ambiguous_width=self.east_asian_ambiguous_width
        )

        return self.__dp_converter.convert(dp)

    def __to_dataproperty_list(
            self, data_list, type_hint=None, strict_type_mapping=None):
        if is_empty_sequence(data_list):
            return []

        return [
            self.__to_dataproperty(data, type_hint, strict_type_mapping)
            for data in data_list
        ]

    def __get_col_dp_list_base(self):
        header_dp_list = self.to_header_dataproperty_list()
        col_dp_list = []

        for header_dp in header_dp_list:
            col_dp = ColumnDataProperty(
                min_padding_len=self.min_padding_len,
                datetime_format_str=self.datetime_format_str,
                east_asian_ambiguous_width=self.east_asian_ambiguous_width
            )
            col_dp.update_header(header_dp)
            col_dp_list.append(col_dp)

        return col_dp_list

    def __update_dp_converter(self):
        self.__dp_converter = DataPropertyConverter(
            type_value_mapping=self.type_value_mapping,
            const_value_mapping=self.const_value_mapping,
            quote_flag_mapping=self.quote_flag_mapping,
            datetime_formatter=self.datetime_formatter,
            datetime_format_str=self.datetime_format_str,
            float_type=self.float_type,
            strict_type_mapping=self.strict_type_mapping)

    def extract_data_property_matrix(self):
        # alias to to_dataproperty_matrix method.
        # this method will be deleted in the future.

        return self.to_dataproperty_matrix()

    def extract_column_property_list(self):
        # alias to to_col_dataproperty_list method.
        # this method will be deleted in the future.

        return self.to_col_dataproperty_list()

    def extract_col_property_list(self):
        # alias to to_col_dataproperty_list method.
        # this method will be deleted in the future.

        return self.to_col_dataproperty_list()

    def extract_data_property_list(self, data_list):
        # alias to to_dataproperty_list method.
        # this method will be deleted in the future.

        return self.to_dataproperty_list(data_list)
