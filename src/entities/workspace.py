from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List
from uuid import UUID

from src.entities.exceptions.invalid_entity_exception import InvalidEntityException
from src.entities.user import User


@dataclass
class Workspace:
    id: UUID
    name: str
    users_ids: List[UUID]

    created_by: User
    updated_by: User
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime]

    def __post_init__(self):
        if not self.name:
            raise InvalidEntityException("Workspace", ["name"])

    def __eq__(self, other):
        return self.id == other.id

    def __hash__(self):
        return hash(self.id)

    def user_has_permission(self, user: User) -> bool:
        if user == self.created_by:
            return True

        return self.users_ids and user.id in self.users_ids
