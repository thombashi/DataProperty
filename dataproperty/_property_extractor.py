# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <gogogo.vm@gmail.com>
"""


from ._data_property import DataProperty
from ._data_property import ColumnDataProperty
from ._function import is_empty_list_or_tuple
from ._function import is_not_empty_list_or_tuple


class PropertyExtractor(object):

    def extract_data_property_matrix(self):
        return [
            self.__extract_data_property_list(data_list)
            for data_list in self.data_matrix
        ]

    def extract_column_property_list(self):
        data_prop_matrix = self.extract_data_property_matrix()
        header_prop_list = self.__extract_data_property_list(self.header_list)
        column_prop_list = []

        for col_idx, col_prop_list in enumerate(zip(*data_prop_matrix)):
            column_prop = ColumnDataProperty(
                min_padding_len=self.min_padding_len)

            if is_not_empty_list_or_tuple(header_prop_list):
                header_prop = header_prop_list[col_idx]
                column_prop.update_header(header_prop)

            for prop in col_prop_list:
                column_prop.update_body(prop)

            column_prop_list.append(column_prop)

        return column_prop_list

    def __init__(self):
        self.header_list = []
        self.data_matrix = []
        self.min_padding_len = 0

    @staticmethod
    def __extract_data_property_list(data_list):
        if is_empty_list_or_tuple(data_list):
            return []

        return [DataProperty(data) for data in data_list]
