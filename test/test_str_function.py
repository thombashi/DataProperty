"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

import itertools

import pytest

from dataproperty import calc_ascii_char_width


nan = float("nan")
inf = float("inf")


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
