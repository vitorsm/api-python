from enum import Enum
from typing import Optional, Type


def instantiate_enum_from_str_name(enum_type: Type[Enum], str_name: str) -> Optional[Enum]:
    return next((enum_item for enum_item in enum_type if enum_item.name ==  str_name), None)
