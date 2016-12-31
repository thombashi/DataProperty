# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <gogogo.vm@gmail.com>
"""

from __future__ import unicode_literals


class Align(object):

    class __AlignData(object):

        @property
        def align_code(self):
            return self.__align_code

        @property
        def align_string(self):
            return self.__align_string

        def __init__(self, code, string):
            self.__align_code = code
            self.__align_string = string

        def __repr__(self):
            return self.align_string

    AUTO = __AlignData(1 << 0, "auto")
    LEFT = __AlignData(1 << 1, "left")
    RIGHT = __AlignData(1 << 2, "right")
    CENTER = __AlignData(1 << 3, "center")
