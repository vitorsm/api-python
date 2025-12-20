from typing import Optional
from uuid import UUID


def to_uuid(str_uuid: Optional[str]) -> Optional[UUID]:
    if not str_uuid:
        return None

    try:
        return UUID(str_uuid)
    except ValueError:
        return None
