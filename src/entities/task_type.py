from dataclasses import dataclass
from typing import List, Optional

from src.entities.generic_entity import GenericEntity


@dataclass
class TaskType(GenericEntity):
    parent_type: Optional['TaskType']

    def _get_invalid_fields(self) -> List[str]:
        if not self.name:
            return ["name"]
        return []
