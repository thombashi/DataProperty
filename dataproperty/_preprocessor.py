# encoding: utf-8

from __future__ import absolute_import, unicode_literals

import re

import six
from mbstrdecoder import MultiByteStrDecoder

from ._function import strip_ansi_escape
from ._line_break import LineBreakHandling


_RE_LINE_BREAK = re.compile(r"\r\n|\n")
_RE_FORMULA_PREFIX = re.compile(r"^[-\+=@]")


def normalize_lbh(value):
    if isinstance(value, LineBreakHandling):
        return value

    if value is None:
        return LineBreakHandling.NOP

    return LineBreakHandling[value.upper()]


class Preprocessor(object):
    @property
    def line_break_handling(self):
        return self.__line_break_handling

    @line_break_handling.setter
    def line_break_handling(self, value):
        self.__line_break_handling = normalize_lbh(value)

    def __init__(
        self,
        strip_str=None,
        replace_tabs_with_spaces=True,
        tab_length=2,
        line_break_handling=None,
        line_break_repl=" ",
        is_escape_html_tag=False,
        is_escape_formula_injection=False,
    ):
        self.strip_str = strip_str
        self.replace_tabs_with_spaces = replace_tabs_with_spaces
        self.tab_length = tab_length
        self.line_break_handling = line_break_handling
        self.line_break_repl = line_break_repl
        self.is_escape_html_tag = is_escape_html_tag
        self.is_escape_formula_injection = is_escape_formula_injection

    def __repr__(self):
        return ", ".join(
            [
                "strip_str={}".format(self.strip_str),
                "replace_tabs_with_spaces={}".format(self.replace_tabs_with_spaces),
                "tab_length={}".format(self.tab_length),
                "line_break_handling={}".format(self.line_break_handling),
                "line_break_repl={}".format(self.line_break_repl),
                "escape_html_tag={}".format(self.is_escape_html_tag),
                "escape_formula_injection={}".format(self.is_escape_formula_injection),
            ]
        )

    def preprocess(self, data):
        data, no_ansi_escape_data = self.__preprocess_string(
            self.__preprocess_data(data, self.strip_str),
        )
        return (data, no_ansi_escape_data)

    def update(self, **kwargs):
        is_update = False

        for key, value in kwargs.items():
            if not hasattr(self, key):
                continue

            if getattr(self, key) == value:
                continue

            setattr(self, key, value)
            is_update = True

        return is_update

    def __preprocess_string(
        self, raw_data,
    ):
        data = raw_data

        if self.replace_tabs_with_spaces:
            try:
                data = data.replace("\t", " " * self.tab_length)
            except (TypeError, AttributeError):
                pass

        if self.is_escape_html_tag:
            if six.PY2:
                import cgi

                data = cgi.escape(data)
            else:
                import html

                try:
                    data = html.escape(data)
                except AttributeError:
                    return (data, None)

        data = self.__process_line_break(data)
        data = self.__escape_formula_injection(data)

        try:
            return (data, strip_ansi_escape(data))
        except TypeError:
            return (data, None)

    @staticmethod
    def __preprocess_data(data, strip_str):
        if strip_str is None:
            return data

        try:
            return data.strip(strip_str)
        except AttributeError:
            return data
        except UnicodeDecodeError:
            return MultiByteStrDecoder(data).unicode_str.strip(strip_str)

    def __process_line_break(self, data):
        lbh = self.line_break_handling

        if lbh == LineBreakHandling.NOP:
            return data

        try:
            if lbh == LineBreakHandling.REPLACE:
                return _RE_LINE_BREAK.sub(self.line_break_repl, data)

            if lbh == LineBreakHandling.ESCAPE:
                return data.replace("\n", "\\n").replace("\r", "\\r")
        except (TypeError, AttributeError):
            return data

        raise ValueError("unexpected line_break_handling: {}".format(lbh))

    def __escape_formula_injection(self, data):
        if not self.is_escape_formula_injection:
            return data

        try:
            if _RE_FORMULA_PREFIX.search(data):
                return "'" + data
        except (TypeError, AttributeError):
            return data

        return data
