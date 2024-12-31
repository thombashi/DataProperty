from collections.abc import Mapping
from datetime import datetime
from decimal import Decimal
from typing import Any, Callable, Final, Optional, Union

from typepy import (
    Bool,
    DateTime,
    Dictionary,
    Infinity,
    Integer,
    IpAddress,
    List,
    Nan,
    NoneType,
    NullString,
    RealNumber,
    String,
    Typecode,
)
from typepy.type import AbstractType


TypeHint = Optional[type[AbstractType]]
TransFunc = Callable[[Any], Any]
DateTimeFormatter = Callable[[datetime], str]

FloatType = Union[type[Decimal], type[float]]
StrictLevelMap = Mapping[Union[str, Typecode], int]
TypeValueMap = dict[Typecode, Union[float, str, Decimal, None]]

_type_hint_map: Final = {
    # high frequently used types
    "int": Integer,
    "float": RealNumber,
    "realnumber": RealNumber,
    "str": String,
    # low frequently used types
    "bool": Bool,
    "datetime": DateTime,
    "dict": Dictionary,
    "inf": Infinity,
    "ip": IpAddress,
    "list": List,
    "nan": Nan,
    "none": NoneType,
    "nullstr": NullString,
}


def normalize_type_hint(type_hint: Union[str, TypeHint]) -> TypeHint:
    if not type_hint:
        return None

    if not isinstance(type_hint, str):
        return type_hint

    type_hint = type_hint.strip().casefold()
    for key, value in _type_hint_map.items():
        if type_hint.startswith(key):
            return value

    raise ValueError(f"unknown typehint: {type_hint}")
