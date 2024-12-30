"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

import abc
from typing import Optional

from typepy import Typecode

from ._align import Align


class DataPeropertyInterface(metaclass=abc.ABCMeta):
    __slots__ = ()

    @property
    @abc.abstractmethod
    def align(self) -> Align:  # pragma: no cover
        pass

    @property
    @abc.abstractmethod
    def decimal_places(self) -> Optional[int]:  # pragma: no cover
        pass

    @property
    @abc.abstractmethod
    def typecode(self) -> Typecode:  # pragma: no cover
        pass

    @property
    @abc.abstractmethod
    def typename(self) -> str:  # pragma: no cover
        pass
