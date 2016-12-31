# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <gogogo.vm@gmail.com>
"""

from __future__ import absolute_import
from __future__ import unicode_literals

from six.moves import zip

from ._common import (
    DEFAULT_INF_VALUE,
    DEFAULT_NAN_VALUE,
    DEFAULT_STRICT_TYPE_MAPPING,
    STRICT_TYPE_MAPPING,
    default_bool_converter,
    default_datetime_converter,
)
from ._dataproperty import (
    DataProperty,
    ColumnDataProperty,
)
from ._function import is_empty_sequence


class MissmatchProcessing(object):
    EXCEPTION = 1 << 1
    TRIM = 1 << 2
    EXTEND = 1 << 3


class DataPropertyExtractor(object):

    def __init__(self):
        self.header_list = []
        self.data_matrix = []
        self.strip_str = None
        self.min_padding_len = 0
        self.none_value = None
        self.inf_value = DEFAULT_INF_VALUE
        self.nan_value = DEFAULT_NAN_VALUE
        self.float_type = None
        self.bool_converter = default_bool_converter
        self.datetime_converter = default_datetime_converter
        self.datetime_format_str = "%Y-%m-%dT%H:%M:%S%z"
        self.strict_type_mapping = dict(DEFAULT_STRICT_TYPE_MAPPING)
        self.east_asian_ambiguous_width = 1

        self.mismatch_processing = MissmatchProcessing.TRIM

    def to_dataproperty_matrix(self):
        return [
            self.to_dataproperty_list(data_list)
            for data_list in self.data_matrix
        ]

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

    def to_dataproperty_list(self, data_list):
        if is_empty_sequence(data_list):
            return []

        return [self.to_dataproperty(data) for data in data_list]

    def to_dataproperty(self, data):
        return DataProperty(
            data,
            strip_str=self.strip_str,
            none_value=self.none_value,
            inf_value=self.inf_value,
            nan_value=self.nan_value,
            float_type=self.float_type,
            bool_converter=self.bool_converter,
            datetime_converter=self.datetime_converter,
            datetime_format_str=self.datetime_format_str,
            strict_type_mapping=self.strict_type_mapping,
            east_asian_ambiguous_width=self.east_asian_ambiguous_width
        )

    def to_header_dataproperty_list(self):
        old_strict_type_mapping = self.strict_type_mapping
        self.strict_type_mapping = STRICT_TYPE_MAPPING

        header_dp_list = self.to_dataproperty_list(self.header_list)

        self.strict_type_mapping = old_strict_type_mapping

        return header_dp_list

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
