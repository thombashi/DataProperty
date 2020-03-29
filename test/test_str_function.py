"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

import itertools

import pytest

from dataproperty import calc_ascii_char_width, is_multibyte_str


nan = float("nan")
inf = float("inf")


class Test_is_multibyte_str:
    @pytest.mark.parametrize(
        ["value", "expected"],
        [
            ["吾輩は猫である", True],
            ["abcdef", False],
            [
                "RKBTqn1G9HIZ9onY9mCklj3+8ye7WBmu0xKMqp3ORT3pMgR5m73VXAR/5YrTZTGer"
                "nMYLCPYdwIMewFY+6xOZmWwCrXjfw3sO2dYLubh9EIMrc/XEvAhMFd969G2yQkyFT"
                "Nf9M8Ag94QCuBk51yQLSbxgmxJTqEw6bdC4gNTI44=",
                False,
            ],
            [None, False],
            ["", False],
            [True, False],
            [[], False],
            [1, False],
        ],
    )
    def test_normal(self, value, expected):
        assert is_multibyte_str(value) == expected


class Test_calc_ascii_char_width:
    @pytest.mark.parametrize(
        ["value", "expected"], [["吾輩は猫である", 14], ["いaろbはc", 9], ["abcdef", 6], ["", 0]]
    )
    def test_normal(self, value, expected):
        assert calc_ascii_char_width(value) == expected

    @pytest.mark.parametrize(
        ["value", "ambiguous_width"],
        itertools.product(["Ø", "α", "β", "γ", "θ", "κ", "λ", "π", "ǎ"], [1, 2]),
    )
    def test_normal_east_asian_ambiguous(self, value, ambiguous_width):
        assert calc_ascii_char_width(value, ambiguous_width) == ambiguous_width

    @pytest.mark.parametrize(
        ["value", "expected"],
        [
            [b"abcdef", TypeError],
            [None, TypeError],
            [True, TypeError],
            [1, TypeError],
            [nan, TypeError],
        ],
    )
    def test_exception(self, value, expected):
        with pytest.raises(expected):
            calc_ascii_char_width(value)
