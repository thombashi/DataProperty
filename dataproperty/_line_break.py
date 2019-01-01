# encoding: utf-8

from __future__ import absolute_import, unicode_literals

import enum


@enum.unique
class LineBreakHandling(enum.Enum):
    NOP = 0
    REPLACE = 1
    ESCAPE = 2
