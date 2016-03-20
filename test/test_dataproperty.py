# encoding: utf-8

'''
@author: Tsuyoshi Hombashi
'''

import datetime

from dataproperty import *
import pytest


nan = float("nan")
inf = float("inf")


class Test_is_integer:

    @pytest.mark.parametrize(["value"], [
        [0], [99999999999], [-99999999999],
        [1234567890123456789], [-1234567890123456789],
        ["0"], ["99999999999"], ["-99999999999"],
        [" 1"], ["1 "],
    ])
    def test_normal(self, value):
        assert is_integer(value)

    @pytest.mark.parametrize(["value"], [
        [None], [nan], [inf],
        [0.5], ["0.5"],
        [.999], [".999"],
        [""], ["test"], ["1a1"], ["11a"], ["a11"],
        [True],
        [1e-05], [-1e-05],
        ["1e-05"], ["-1e-05"],
        [-0.00001],
    ])
    def test_abnormal(self, value):
        assert not is_integer(value)


class Test_is_hex:

    @pytest.mark.parametrize(["value"], [
        ["0x00"], ["0xffffffff"], ["a"], ["f"],
    ])
    def test_normal(self, value):
        assert is_hex(value)

    @pytest.mark.parametrize(["value"], [
        [None], [nan], [inf],
        [0], [1], [0.5],
        ["test"], ["g"],
        [True],
    ])
    def test_abnormal(self, value):
        assert not is_hex(value)


class Test_is_float:

    @pytest.mark.parametrize(["value"], [
        [0.0], [0.1], [-0.1], [1], [-1],
        ["0.0"], ["0.1"], ["-0.1"], ["1"], ["-1"],
        [.5], [0.],
        ["1e-05"],
        [nan], [inf],
    ])
    def test_normal(self, value):
        assert is_float(value)

    @pytest.mark.parametrize(["value"], [
        [None],
        ["test"],
        ["inf"],
        [True],
    ])
    def test_abnormal(self, value):
        assert not is_float(value)


class Test_is_nan:

    @pytest.mark.parametrize(["value", "expected"], [
        [nan, True],

        [None, False],
        ["nan", False],
        ["１", False],
        [inf, False],
        [1, False],
        [0.1, False],
        [True, False],
    ])
    def test_normal(self, value, expected):
        assert is_nan(value) == expected


class Test_is_not_empty_string:

    @pytest.mark.parametrize(["value", "expected"], [
        ["nan", True],
        ["テスト", True],

        [None, False],
        ["", False],
        ["  ", False],
        ["\t", False],
        ["\n", False],
        [[], False],
        [1, False],
        [True, False],
    ])
    def test_normal(self, value, expected):
        assert is_not_empty_string(value) == expected


class Test_is_empty_string:

    @pytest.mark.parametrize(["value", "expected"], [
        ["nan", False],
        ["テスト", False],

        [None, True],
        ["", True],
        ["  ", True],
        ["\t", True],
        ["\n", True],
        [True, True],
        [[], True],
        [1, True],
    ])
    def test_normal(self, value, expected):
        assert is_empty_string(value) == expected


class Test_is_list_or_tuple:

    @pytest.mark.parametrize(["value", "expected"], [
        [[], True],
        [[1], True],
        [["a"] * 200000, True],
        [(), True],
        [(1,), True],
        [("a",) * 200000, True],

        [None, False],
        [nan, False],
        [0, False],
        ["aaa", False],
        [True, False],
    ])
    def test_normal(self, value, expected):
        assert is_list_or_tuple(value) == expected


class Test_is_empty_list_or_tuple:

    @pytest.mark.parametrize(["value", "expected"], [
        [(), True],
        [[], True],
        [None, True],

        [[1], False],
        [["a"] * 200000, False],
        [(1,), False],
        [("a",) * 200000, False],
    ])
    def test_normal(self, value, expected):
        assert is_empty_list_or_tuple(value) == expected

    @pytest.mark.parametrize(["value", "expected"], [
        [nan, False],
        [0, False],
        ["aaa", False],
        [True, False],
    ])
    def test_abnormal(self, value, expected):
        assert is_empty_list_or_tuple(value) == expected


class Test_is_not_empty_list_or_tuple:

    @pytest.mark.parametrize(["value", "expected"], [
        [(), False],
        [[], False],
        [None, False],

        [[1], True],
        [["a"] * 200000, True],
        [(1,), True],
        [("a",) * 200000, True],
    ])
    def test_normal(self, value, expected):
        assert is_not_empty_list_or_tuple(value) == expected

    @pytest.mark.parametrize(["value", "expected"], [
        [nan, False],
        [0, False],
        ["aaa", False],
        [True, False],
    ])
    def test_abnormal(self, value, expected):
        assert is_not_empty_list_or_tuple(value) == expected


class Test_is_datetime:

    @pytest.mark.parametrize(["value", "expected"], [
        [datetime.datetime(2016, 1, 1), True],

        [None, False],
        ["", False],
        ["テスト", False],
        [[], False],
        [1, False],
        [True, False],
    ])
    def test_normal(self, value, expected):
        assert is_datetime(value) == expected


class Test_get_integer_digit:

    @pytest.mark.parametrize(["value", "expected"], [
        [0, 1], [-0, 1],
        [.99, 1], [-.99, 1],
        [".99", 1], ["-.99", 1],
        [1.01, 1], [-1.01, 1],
        [9.99, 1], [-9.99, 1],
        ["9.99", 1], ["-9.99", 1],
        ["0", 1], ["-0", 1],

        [10, 2], [-10, 2],
        [99.99, 2], [-99.99, 2],
        ["10", 2], ["-10", 2],
        ["99.99", 2], ["-99.99", 2],

        [100, 3], [-100, 3],
        [999.99, 3], [-999.99, 3],
        ["100", 3], ["-100", 3],
        ["999.99", 3], ["-999.99", 3],

        [10000000000000000000, 20], [-10000000000000000000, 20],
        [99999999999999099999.99, 20], [-99999999999999099999.99, 20],
        ["10000000000000000000", 20], ["-10000000000000000000", 20],
        ["99999999999999099999.99", 20], ["-99999999999999099999.99", 20],

        [True, 1],
        [False, 1],
    ])
    def test_normal(self, value, expected):
        assert get_integer_digit(value) == expected

    @pytest.mark.parametrize(["value", "expected"], [
        [99999999999999999999.99, 21],
        [-99999999999999999999.99, 21],
        ["99999999999999999999.99", 21],
        ["-99999999999999999999.99", 21],
    ])
    def test_abnormal(self, value, expected):
        # expected result == 20
        assert get_integer_digit(value) == expected

    @pytest.mark.parametrize(["value", 'exception'], [
        [None, TypeError],
        ["test", ValueError],
        ["a", ValueError],
        ["0xff", ValueError],
        [nan, ValueError],
        [inf, OverflowError],
    ])
    def test_exception(self, value, exception):
        with pytest.raises(exception):
            get_integer_digit(value)


class Test_get_number_of_digit:

    @pytest.mark.parametrize(["value", "expected"], [
        [0, (1, 0)], [-0, (1, 0)],
        ["0", (1, 0)], ["-0", (1, 0)],
        [10, (2, 0)], [-10, (2, 0)],
        ["10", (2, 0)], ["-10", (2, 0)],
        [10.1, (2, 1)], [-10.1, (2, 1)],
        ["10.1", (2, 1)], ["-10.1", (2, 1)],
        [10.01, (2, 2)], [-10.01, (2, 2)],
        [10.001, (2, 2)], [-10.001, (2, 2)],
        [100.1, (3, 1)], [-100.1, (3, 1)],
        [100.01, (3, 1)], [-100.01, (3, 1)],
        [0.1, (1, 1)], [-0.1, (1, 1)],
        ["0.1", (1, 1)], ["-0.1", (1, 1)],
        [.99, (1, 2)], [-.99, (1, 2)],
        [".99", (1, 2)], ["-.99", (1, 2)],
        [0.01, (1, 2)], [-0.01, (1, 2)],
        ["0.01", (1, 2)], ["-0.01", (1, 2)],
        [0.001, (1, 3)], [-0.001, (1, 3)],
        ["0.001", (1, 3)], ["-0.001", (1, 3)],
        [0.0001, (1, 4)], [-0.0001, (1, 4)],
        ["0.0001", (1, 4)], ["-0.0001", (1, 4)],
        [0.00001, (1, 4)], [-0.00001, (1, 4)],
        ["0.00001", (1, 4)], ["-0.00001", (1, 4)],
        [2e-05, (1, 4)], [-2e-05, (1, 4)],
        ["2e-05", (1, 4)], ["-2e-05", (1, 4)],
    ])
    def test_normal(self, value, expected):
        assert get_number_of_digit(value) == expected

    @pytest.mark.parametrize(["value", "expected1", "expected2"], [
        [True, 1, 1],
    ])
    def test_annormal(self, value, expected1, expected2):
        sig_digit, float_digit = get_number_of_digit(value)
        assert sig_digit == expected1
        assert float_digit == expected2

    @pytest.mark.parametrize(["value"], [
        [None],
        ["0xff"], ["test"], ["テスト"],
    ])
    def test_abnormal(self, value):
        sig_digit, float_digit = get_number_of_digit(value)
        assert is_nan(sig_digit)
        assert is_nan(float_digit)


class Test_get_text_len:

    def test_normal_1(self):
        assert get_text_len("") == 0
        assert get_text_len(
            "aaaaaaaaaaaaaaaaaaaa"
            "aaaaaaaaaaaaaaaaaaaa"
            "aaaaaaaaaaaaaaaaaaaa"
            "aaaaaaaaaaaaaaaaaaaa"
            "aaaaaaaaaaaaaaaaaaaa"
        ) == 100

    def test_normal_2(self):
        assert get_text_len(u"あ") == 1

    def test_abnormal_1(self):
        assert get_text_len(None) == 4

    def test_abnormal_2(self):
        assert get_text_len(nan) == 3
        assert get_text_len(inf) == 3
