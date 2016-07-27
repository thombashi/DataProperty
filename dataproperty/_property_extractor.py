# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <gogogo.vm@gmail.com>
"""

from six.moves import zip

from ._data_property import DataProperty
from ._data_property import ColumnDataProperty
from ._function import is_empty_sequence


class PropertyExtractor(object):

    def __init__(self):
        from ._data_property import default_bool_converter
        from ._data_property import default_datetime_converter

        self.header_list = []
        self.data_matrix = []
        self.min_padding_len = 0
        self.none_value = None
        self.inf_value = float("inf")
        self.nan_value = float("nan")
        self.bool_converter = default_bool_converter
        self.datetime_converter = default_datetime_converter
        self.datetime_format_str = "%Y-%m-%dT%H:%M:%S%z"
        self.is_convert = True

    def extract_data_property_matrix(self):
        return [
            self.__extract_data_property_list(data_list)
            for data_list in self.data_matrix
        ]

    def extract_column_property_list(self):
        header_prop_list = self.__extract_data_property_list(self.header_list)
        column_prop_list = []

        for header_prop in header_prop_list:
            column_prop = ColumnDataProperty(
                min_padding_len=self.min_padding_len,
                datetime_format_str=self.datetime_format_str)
            column_prop.update_header(header_prop)
            column_prop_list.append(column_prop)

        try:
            data_prop_matrix = self.extract_data_property_matrix()
        except TypeError:
            return column_prop_list

        for col_idx, col_prop_list in enumerate(zip(*data_prop_matrix)):
            try:
                column_prop_list[col_idx]
            except IndexError:
                column_prop_list.append(
                    ColumnDataProperty(
                        min_padding_len=self.min_padding_len,
                        datetime_format_str=self.datetime_format_str))

            for prop in col_prop_list:
                column_prop_list[col_idx].update_body(prop)

        return column_prop_list

    def __extract_data_property_list(self, data_list):
        if is_empty_sequence(data_list):
            return []

        return [
            DataProperty(
                data,
                none_value=self.none_value,
                inf_value=self.inf_value,
                nan_value=self.nan_value,
                bool_converter=self.bool_converter,
                datetime_converter=self.datetime_converter,
                datetime_format_str=self.datetime_format_str,
                is_convert=self.is_convert)
            for data in data_list
        ]
