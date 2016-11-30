# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <gogogo.vm@gmail.com>
"""

import itertools

from dataproperty import *
import pytest
import six


nan = float("nan")
inf = float("inf")


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
        [nan, False],
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


class Test_to_unicode:

    @pytest.mark.parametrize(["value", "expected"], [
        [u"吾輩は猫である", u"吾輩は猫である"],
        ["吾輩は猫である", u"吾輩は猫である"],
        ["マルチバイト文字", u"マルチバイト文字"],
        ["abcdef", u"abcdef"],
        [None, u"None"],
        ["", u""],
        [True, u"True"],
        [[], u"[]"],
        [1, u"1"],
    ])
    def test_normal(self, value, expected):
        unicode_str = to_unicode(value)

        assert unicode_str == expected
        assert to_unicode(unicode_str) == unicode_str


class Test_is_multibyte_str:

    @pytest.mark.parametrize(["value", "expected"], [
        [u"吾輩は猫である", True],
        ["吾輩は猫である", True],
        ["abcdef", False],
        [None, False],
        ["", False],
        [True, False],
        [[], False],
        [1, False],
    ])
    def test_normal(self, value, expected):
        assert is_multibyte_str(value) == expected


class Test_get_ascii_char_width:

    @pytest.mark.parametrize(["value", "expected"], [
        [u"吾輩は猫である", 14],
        [u"いaろbはc", 9],
        [u"abcdef", 6],
        [u"", 0],
    ])
    def test_normal(self, value, expected):
        assert get_ascii_char_width(value) == expected

    @pytest.mark.parametrize(
        ["value", "ambiguous_width"],
        itertools.product(
            [u"Ø", u"α", u"β", u"γ", u"θ", u"κ", u"λ", u"π", u"ǎ"],
            [1, 2])
    )
    def test_normal_east_asian_ambiguous(
            self, value, ambiguous_width):
        assert get_ascii_char_width(value, ambiguous_width) == ambiguous_width

    @pytest.mark.parametrize(["value", "expected"], [
        [six.b("abcdef"), TypeError],
        [None, TypeError],
        [True, TypeError],
        [1, TypeError],
        [nan, TypeError],
    ])
    def test_exception(self, value, expected):
        with pytest.raises(expected):
            get_ascii_char_width(value)
