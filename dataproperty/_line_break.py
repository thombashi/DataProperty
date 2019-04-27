# encoding: utf-8

from __future__ import absolute_import, unicode_literals

from enum import Enum, auto, unique


@unique
class LineBreakHandling(Enum):
    NOP = auto()
    REPLACE = auto()
    ESCAPE = auto()
