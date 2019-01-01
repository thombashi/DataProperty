# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

from __future__ import absolute_import

from .__version__ import __author__, __copyright__, __email__, __license__, __version__
from ._align import Align
from ._align_getter import align_getter
from ._column import ColumnDataProperty
from ._common import NOT_QUOTING_FLAGS, NOT_STRICT_TYPE_MAP, STRICT_TYPE_MAP, DefaultValue
from ._container import MinMaxContainer
from ._dataproperty import DataProperty
from ._extractor import DataPropertyExtractor, MatrixFormatting
from ._formatter import Format
from ._function import (
    calc_ascii_char_width,
    get_integer_digit,
    get_number_of_digit,
    is_multibyte_str,
)
from ._line_break import LineBreakHandling
from ._logger import set_log_level, set_logger
