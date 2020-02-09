# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

from __future__ import absolute_import, unicode_literals

from ._null_logger import NullLogger


MODULE_NAME = "dataproperty"

try:
    from loguru import logger

    logger.disable(MODULE_NAME)
    LOGURU_INSTALLED = True
except ImportError:
    logger = NullLogger()
    LOGURU_INSTALLED = False


def set_logger(is_enable):
    if is_enable:
        logger.enable(MODULE_NAME)
    else:
        logger.disable(MODULE_NAME)


def set_log_level(log_level):
    # deprecated
    return
