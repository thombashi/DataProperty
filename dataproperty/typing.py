from decimal import Decimal
from typing import Any, Callable, Mapping, Optional, Type, Union

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


StrictLevelMap = Mapping[Union[str, Typecode], int]
TypeHint = Optional[Type[AbstractType]]
TransFunc = Callable[[Any], Any]

FloatType = Union[Type[Decimal], Type[float]]

_type_hint_map = {
    "bool": Bool,
    "datetime": DateTime,
    "dict": Dictionary,
    "dictionary": Dictionary,
    "inf": Infinity,
    "infinity": Infinity,
    "int": Integer,
    "integer": Integer,
    "ip": IpAddress,
    "ipaddr": IpAddress,
    "ipaddress": IpAddress,
    "list": List,
    "nan": Nan,
    "none": NoneType,
    "nullstr": NullString,
    "nullstring": NullString,
    "realnumber": RealNumber,
    "str": String,
    "string": String,
}


def normalize_type_hint(type_hint: Union[str, TypeHint]) -> TypeHint:
    if not type_hint:
        return None

    if isinstance(type_hint, str):
        return _type_hint_map[type_hint.casefold()]

    return type_hint
