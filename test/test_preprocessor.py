# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

from __future__ import unicode_literals

from dataproperty import LineBreakHandling, Preprocessor


class Test_Preprocessor_update(object):
    def test_normal(self):
        preprocessor = Preprocessor()
        assert preprocessor.strip_str is None
        assert preprocessor.replace_tabs_with_spaces is True
        assert preprocessor.tab_length == 2
        assert preprocessor.line_break_handling is LineBreakHandling.NOP
        assert preprocessor.line_break_repl == " "
        assert preprocessor.is_escape_html_tag is False
        assert preprocessor.is_escape_formula_injection is False

        assert preprocessor.update(
            strip_str='"',
            replace_tabs_with_spaces=False,
            tab_length=4,
            line_break_handling=LineBreakHandling.REPLACE,
            line_break_repl="<br>",
            is_escape_html_tag=True,
            is_escape_formula_injection=True,
        )
        assert preprocessor.strip_str == '"'
        assert preprocessor.replace_tabs_with_spaces is False
        assert preprocessor.tab_length == 4
        assert preprocessor.line_break_handling is LineBreakHandling.REPLACE
        assert preprocessor.line_break_repl == "<br>"
        assert preprocessor.is_escape_html_tag is True
        assert preprocessor.is_escape_formula_injection is True

        assert not preprocessor.update(strip_str='"')
