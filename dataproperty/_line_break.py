# encoding: utf-8

from __future__ import absolute_import, unicode_literals

from enum import Enum, unique


@unique
class LineBreakHandling(Enum):
    NOP = 0
    REPLACE = 1
    ESCAPE = 2
