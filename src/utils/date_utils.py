from datetime import datetime
from typing import Optional


def iso_to_datetime(iso_str: Optional[str]) -> Optional[datetime]:
    if not iso_str:
        return None

    try:
        return datetime.fromisoformat(iso_str)
    except ValueError:
        return None


def datetime_to_iso(_datetime: Optional[datetime]) -> Optional[str]:
    if not _datetime:
        return None

    return _datetime.isoformat()
