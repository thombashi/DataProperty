"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

import pytest

from dataproperty import LineBreakHandling, Preprocessor


class Test_Preprocessor_update:
    def test_normal(self):
        preprocessor = Preprocessor()
        assert preprocessor.strip_str is None
        assert preprocessor.replace_tabs_with_spaces is True
        assert preprocessor.tab_length == 2
        assert preprocessor.line_break_handling is LineBreakHandling.NOP
        assert preprocessor.line_break_repl == " "
        assert preprocessor.dequote is False
        assert preprocessor.is_escape_html_tag is False
        assert preprocessor.is_escape_formula_injection is False

        assert preprocessor.update(
            strip_str='"',
            replace_tabs_with_spaces=False,
            tab_length=4,
            line_break_handling=LineBreakHandling.REPLACE,
            line_break_repl="<br>",
            dequote=True,
            is_escape_html_tag=True,
            is_escape_formula_injection=True,
        )
        assert preprocessor.strip_str == '"'
        assert preprocessor.replace_tabs_with_spaces is False
        assert preprocessor.tab_length == 4
        assert preprocessor.line_break_handling is LineBreakHandling.REPLACE
        assert preprocessor.line_break_repl == "<br>"
        assert preprocessor.dequote is True
        assert preprocessor.is_escape_html_tag is True
        assert preprocessor.is_escape_formula_injection is True

        assert not preprocessor.update(strip_str='"')
        assert preprocessor.update(strip_str="")


class Test_Preprocessor_preprocess:
    @pytest.mark.parametrize(
        ["value", "expected"],
        [
            ['abc "efg"', 'abc "efg"'],
            ['"abc efg"', "abc efg"],
            ["'abc efg'", "abc efg"],
            ['"abc" "efg"', '"abc" "efg"'],
            ["'abc' 'efg'", "'abc' 'efg'"],
            ["\"abc 'efg'\"", "abc 'efg'"],
        ],
    )
    def test_normal_dequote(self, value, expected):
        preprocessor = Preprocessor(
            dequote=True,
        )
        data, no_ansi_escape_data = preprocessor.preprocess(value)
        assert data == expected


class Test_Preprocessor_preprocess_string:
    @pytest.mark.parametrize(
        ["value", "expected"],
        [
            [{"1": 1}, {"1": 1}],
            [{"1"}, {"1"}],
        ],
    )
    def test_not_str(self, value, expected):
        preprocessor = Preprocessor(dequote=True)
        data, _ = preprocessor._Preprocessor__preprocess_string(value)
        assert data == expected
