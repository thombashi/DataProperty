# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

from __future__ import absolute_import, unicode_literals

from ._null_logger import NullLogger


def _disable_logger(l):
    try:
        l.disable()
    except AttributeError:
        l.disabled = True  # to support Logbook<1.0.0


try:
    import logbook

    logger = logbook.Logger("DataProperty")
    _disable_logger(logger)
    LOGBOOK_INSTALLED = True
except ImportError:
    logger = NullLogger()
    LOGBOOK_INSTALLED = False


def set_logger(is_enable):
    if not LOGBOOK_INSTALLED:
        return

    if is_enable:
        try:
            logger.enable()
        except AttributeError:
            logger.disabled = False  # to support Logbook<1.0.0
    else:
        _disable_logger(logger)


def set_log_level(log_level):
    """
    Set logging level of this module. The module using
    `logbook <https://logbook.readthedocs.io/en/stable/>`__ module for logging.

    :param int log_level:
        One of the log level of the
        `logbook <https://logbook.readthedocs.io/en/stable/api/base.html>`__.
        Disabled logging if the ``log_level`` is ``logbook.NOTSET``.
    :raises LookupError: If ``log_level`` is an invalid value.
    """

    if not LOGBOOK_INSTALLED:
        return

    # validate log level
    logbook.get_level_name(log_level)

    if log_level == logger.level:
        return

    if log_level == logbook.NOTSET:
        set_logger(is_enable=False)
    else:
        set_logger(is_enable=True)

    logger.level = log_level
