from typing import Any, Callable, Mapping, Optional, Type, Union

from typepy import Typecode
from typepy.type import AbstractType


StrictLevelMap = Mapping[Union[str, Typecode], int]
TypeHint = Optional[Type[AbstractType]]
TransFunc = Callable[[Any], Any]
