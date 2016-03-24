# encoding: utf-8

'''
@author: Tsuyoshi Hombashi
'''


from dataproperty import *
import pytest


class Test_AlignGetter_get_align_from_typecode:

    @pytest.mark.parametrize(["value", "expected"], [
        [Typecode.STRING, Align.LEFT],
        [Typecode.INT, Align.RIGHT],
        [Typecode.FLOAT, Align.RIGHT],
        [Typecode.NONE, Align.LEFT],
    ])
    def test_normal(self, value, expected):
        assert align_getter.get_align_from_typecode(value) == expected
