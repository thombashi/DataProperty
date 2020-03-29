"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

import pytest
from typepy import Typecode

from dataproperty import Align
from dataproperty._align_getter import AlignGetter


@pytest.fixture
def align_getter():
    return AlignGetter()


class Test_AlignGetter_get_align_from_typecode:
    @pytest.mark.parametrize(
        ["value", "expected"],
        [
            [Typecode.STRING, Align.LEFT],
            [Typecode.INTEGER, Align.RIGHT],
            [Typecode.REAL_NUMBER, Align.RIGHT],
            [Typecode.NONE, Align.LEFT],
        ],
    )
    def test_normal(self, align_getter, value, expected):
        assert align_getter.get_align_from_typecode(value) == expected

    @pytest.mark.parametrize(
        ["value", "expected"],
        [
            [Typecode.STRING, Align.RIGHT],
            [Typecode.INTEGER, Align.LEFT],
            [Typecode.REAL_NUMBER, Align.CENTER],
            [Typecode.NONE, Align.LEFT],
        ],
    )
    def test_setter(self, align_getter, value, expected):
        align_getter.typecode_align_table = {
            Typecode.STRING: Align.RIGHT,
            Typecode.INTEGER: Align.LEFT,
            Typecode.REAL_NUMBER: Align.CENTER,
        }

        assert align_getter.get_align_from_typecode(value) == expected

    @pytest.mark.parametrize(
        ["value", "expected"],
        [
            [Typecode.STRING, Align.LEFT],
            [Typecode.INTEGER, Align.RIGHT],
            [Typecode.REAL_NUMBER, Align.RIGHT],
            [Typecode.NONE, Align.CENTER],
        ],
    )
    def test_default_align(self, align_getter, value, expected):
        align_getter.default_align = Align.CENTER

        assert align_getter.get_align_from_typecode(value) == expected
