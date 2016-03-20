# encoding: utf-8

'''
@author: Tsuyoshi Hombashi
'''


from dataproperty import *
import pytest


nan = float("nan")
inf = float("inf")


class Test_DataPeroperty_data:

    @pytest.mark.parametrize(["value", "expected"], [
        [1, 1],
        ["a", "a"],
        [None, None],
    ])
    def test_normal(self, value, expected):
        dp = DataPeroperty(value)
        assert dp.data == expected


class Test_DataPeroperty_typecode:

    @pytest.mark.parametrize(["value", "expected"], [
        [1, Typecode.INT],
        [1.0, Typecode.FLOAT],
        [123.45, Typecode.FLOAT],
        ["a", Typecode.STRING],
        [None, Typecode.NONE],
        [nan, Typecode.FLOAT],
    ])
    def test_normal(self, value, expected):
        dp = DataPeroperty(value)
        assert dp.typecode == expected


class Test_DataPeroperty_align:

    @pytest.mark.parametrize(["value", "expected"], [
        [1, Align.RIGHT],
        [1.0, Align.RIGHT],
        ["a", Align.LEFT],
        [None, Align.LEFT],
        [nan, Align.RIGHT],
    ])
    def test_normal(self, value, expected):
        dp = DataPeroperty(value)
        assert dp.align == expected


class Test_DataPeroperty_str_len:

    @pytest.mark.parametrize(["value", "expected"], [
        [1, 1],
        [-1, 2],
        [1.0, 3],
        [-1.0, 4],
        [12.34, 5],

        ["000", 1],
        ["123456789", 9],
        ["-123456789", 10],

        ["a", 1],
        [None, 4],
    ])
    def test_normal(self, value, expected):
        dp = DataPeroperty(value)
        assert dp.str_len == expected

    @pytest.mark.parametrize(["value", "expected"], [
        [nan, nan],
    ])
    def test_abnormal(self, value, expected):
        dp = DataPeroperty(value)
        is_nan(dp.str_len)


class Test_DataPeroperty_integer_digits:

    @pytest.mark.parametrize(["value", "expected"], [
        [1, 1],
        [1.0, 1],
        [12.34, 2],
    ])
    def test_normal(self, value, expected):
        dp = DataPeroperty(value)
        assert dp.integer_digits == expected

    @pytest.mark.parametrize(["value"], [
        [None],
        ["a"],
        [nan],
    ])
    def test_abnormal(self, value):
        dp = DataPeroperty(value)
        is_nan(dp.integer_digits)


class Test_DataPeroperty_decimal_places:

    @pytest.mark.parametrize(["value", "expected"], [
        [1, 0],
        [1.0, 1],
        [12.34, 2],
    ])
    def test_normal(self, value, expected):
        dp = DataPeroperty(value)
        assert dp.decimal_places == expected

    @pytest.mark.parametrize(["value"], [
        [None],
        ["a"],
        [nan],
    ])
    def test_abnormal(self, value):
        dp = DataPeroperty(value)
        is_nan(dp.decimal_places)


class Test_DataPeroperty_additional_format_len:

    @pytest.mark.parametrize(["value", "expected"], [
        [2147483648, 0],
        [0, 0],
        [-1, 1],
        [-0.01, 1],
        ["2147483648", 0],
        ["1", 0],
        ["-1", 1],
        ["-0.01", 1],

        [None, 0],
        ["a", 0],
        [nan, 0],
    ])
    def test_normal(self, value, expected):
        dp = DataPeroperty(value)
        assert dp.additional_format_len == expected


class Test_ColumnDataPeroperty_decimal_places:

    def test_null(self):
        col_prop = ColumnDataPeroperty()
        assert is_nan(col_prop.decimal_places)


class Test_PropertyExtractor_get_align_from_typecode:

    @pytest.mark.parametrize(["value", "expected"], [
        [Typecode.STRING, Align.LEFT],
        [Typecode.INT, Align.RIGHT],
        [Typecode.FLOAT, Align.RIGHT],
    ])
    def test_normal(self, value, expected):
        assert PropertyExtractor.get_align_from_typecode(value) == expected


class Test_PropertyExtractor_extract_data_property_matrix:

    @pytest.mark.parametrize(["value"], [
        [
            [
                [None, 1],
                [1.1, "a"],
            ],
        ],
    ])
    def test_normal(self, value):
        prop_matrix = PropertyExtractor.extract_data_property_matrix(value)

        assert len(prop_matrix) == 2

        prop = prop_matrix[0][0]
        assert prop.typecode == Typecode.NONE
        assert prop.align.align_code == Align.LEFT.align_code
        assert prop.align.align_string == Align.LEFT.align_string
        assert prop.str_len == 4
        assert is_nan(prop.decimal_places)
        assert prop.format_str == "s"

        prop = prop_matrix[0][1]
        assert prop.typecode == Typecode.INT
        assert prop.align.align_code == Align.RIGHT.align_code
        assert prop.align.align_string == Align.RIGHT.align_string
        assert prop.str_len == 1
        assert prop.decimal_places == 0
        assert prop.format_str == "d"

        prop = prop_matrix[1][0]
        assert prop.typecode == Typecode.FLOAT
        assert prop.align.align_code == Align.RIGHT.align_code
        assert prop.align.align_string == Align.RIGHT.align_string
        assert prop.str_len == 3
        assert prop.decimal_places == 1
        assert prop.format_str == ".1f"

        prop = prop_matrix[1][1]
        assert prop.typecode == Typecode.STRING
        assert prop.align.align_code == Align.LEFT.align_code
        assert prop.align.align_string == Align.LEFT.align_string
        assert prop.str_len == 1
        assert is_nan(prop.decimal_places)
        assert prop.format_str == "s"

    @pytest.mark.parametrize(["value", "expected"], [
        [None, TypeError],
    ])
    def test_exception(self, value, expected):
        with pytest.raises(expected):
            PropertyExtractor.extract_data_property_matrix(value)


class Test_PropertyExtractor_extract_column_property_list:
    TEST_DATA_MATRIX = [
        [1, 1.1, "aa",  1,   1],
        [2, 2.2, "bbb", 2.2, 2.2],
        [3, 3.33, "cccc", -3, "ccc"],
    ]

    @pytest.mark.parametrize(["header_list", "value"], [
        [
            ["i", "f", "s", "if", "mix"],
            TEST_DATA_MATRIX,
        ],
        [
            None,
            TEST_DATA_MATRIX,
        ],
        [
            [],
            TEST_DATA_MATRIX,
        ],
    ])
    def test_normal(self, header_list, value):
        col_prop_list = PropertyExtractor.extract_column_property_list(
            header_list, value)

        assert len(col_prop_list) == 5

        prop = col_prop_list[0]
        assert prop.typecode == Typecode.INT
        assert prop.align.align_code == Align.RIGHT.align_code
        assert prop.align.align_string == Align.RIGHT.align_string
        assert prop.padding_len == 1
        assert is_nan(prop.decimal_places)
        assert prop.format_str == "d"

        prop = col_prop_list[1]
        assert prop.typecode == Typecode.FLOAT
        assert prop.align.align_code == Align.RIGHT.align_code
        assert prop.align.align_string == Align.RIGHT.align_string
        assert prop.padding_len == 4
        assert prop.decimal_places == 2
        assert prop.format_str == ".2f"

        prop = col_prop_list[2]
        assert prop.typecode == Typecode.STRING
        assert prop.align.align_code == Align.LEFT.align_code
        assert prop.align.align_string == Align.LEFT.align_string
        assert prop.padding_len == 4
        assert is_nan(prop.decimal_places)
        assert prop.format_str == "s"

        prop = col_prop_list[3]
        assert prop.typecode == Typecode.FLOAT
        assert prop.align.align_code == Align.RIGHT.align_code
        assert prop.align.align_string == Align.RIGHT.align_string
        assert prop.padding_len == 3
        assert prop.decimal_places == 1
        assert prop.format_str == ".1f"

        prop = col_prop_list[4]
        assert prop.typecode == Typecode.STRING
        assert prop.align.align_code == Align.LEFT.align_code
        assert prop.align.align_string == Align.LEFT.align_string
        assert prop.padding_len == 3
        assert prop.decimal_places == 1
        assert prop.format_str == "s"

    @pytest.mark.parametrize(["header_list", "value", "expected"], [
        [
            None,
            None,
            TypeError
        ],
        [
            ["i", "f", "s", "if", "mix"],
            None,
            TypeError
        ],
    ])
    def test_exception(self, header_list, value, expected):
        with pytest.raises(expected):
            PropertyExtractor.extract_column_property_list(
                header_list, value)
