# encoding: utf-8

from __future__ import absolute_import, unicode_literals

import re

import six
from mbstrdecoder import MultiByteStrDecoder

from ._function import strip_ansi_escape
from ._line_break import LineBreakHandling


_RE_LINE_BREAK = re.compile("[\r\n]+")


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
        is_escape_html_tag=False,
    ):
        self.strip_str = strip_str
        self.replace_tabs_with_spaces = replace_tabs_with_spaces
        self.tab_length = tab_length
        self.line_break_handling = line_break_handling
        self.is_escape_html_tag = is_escape_html_tag

    def __repr__(self):
        return ", ".join(
            [
                "strip_str={}".format(self.strip_str),
                "replace_tabs_with_spaces={}".format(self.replace_tabs_with_spaces),
                "tab_length={}".format(self.tab_length),
                "line_break_handling={}".format(self.line_break_handling),
                "is_escape_html_tag={}".format(self.is_escape_html_tag),
            ]
        )

    def preprocess(self, data):
        data, no_ansi_escape_data = self.__preprocess_string(
            self.__process_line_break(self.__preprocess_data(data, self.strip_str)),
        )
        return (data, no_ansi_escape_data)

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
                return _RE_LINE_BREAK.sub(" ", data)

            if lbh == LineBreakHandling.ESCAPE:
                return data.replace("\n", "\\n").replace("\r", "\\r")
        except (TypeError, AttributeError):
            return data

        raise ValueError("unexpected line_break_handling: {}".format(lbh))
