from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from uuid import UUID


from src.entities.exceptions.invalid_entity_exception import InvalidEntityException


@dataclass
class User:
    id: UUID
    name: str
    login: str
    password: str
    email: str
    photo: Optional[str]
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None

    def __post_init__(self):
        invalid_fields = []

        if not self.name:
            invalid_fields.append("name")

        if not self.login:
            invalid_fields.append("login")

        if invalid_fields:
            raise InvalidEntityException("User", invalid_fields)

    def __eq__(self, other):
        return self.id == other.id

    def __hash__(self):
        return hash(self.id)
