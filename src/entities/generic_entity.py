import abc
from dataclasses import dataclass
import datetime
from typing import Optional, List
from uuid import UUID

from src.entities.exceptions.invalid_entity_exception import InvalidEntityException
from src.entities.user import User
from src.entities.workspace import Workspace


@dataclass
class GenericEntity(metaclass=abc.ABCMeta):
    id: UUID
    name: str
    workspace: Workspace
    created_by: User
    updated_by: User
    created_at: datetime.datetime
    updated_at: datetime.datetime
    deleted_at: Optional[datetime]

    def __eq__(self, other):
        return self.id == other.id

    def __hash__(self):
        return hash(self.id)

    @abc.abstractmethod
    def _get_invalid_fields(self) -> List[str]:
        raise NotImplementedError

    def __post_init__(self):
        invalid_fields = self._get_invalid_fields()

        if not self.workspace or not self.workspace.id:
            invalid_fields.append('workspace')

        if invalid_fields:
            raise InvalidEntityException(self.__class__.__name__, invalid_fields)

    def update_audit_fields(self, user: User, is_create: bool = False):
        self.updated_at = datetime.datetime.now(datetime.timezone.utc)
        self.updated_by = user

        if is_create or not self.created_by:
            self.created_by = user
            self.created_at = self.updated_at

    def update_original_fields(self, original_entity: 'GenericEntity'):
        self.created_by = original_entity.created_by
        self.created_at = original_entity.created_at
        self.updated_by = original_entity.updated_by
        self.updated_at = original_entity.updated_at
        self.deleted_at = original_entity.deleted_at
