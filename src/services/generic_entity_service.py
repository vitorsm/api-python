import abc
from typing import TypeVar

from src.entities.exceptions.invalid_entity_exception import InvalidEntityException
from src.entities.exceptions.permission_exception import PermissionException
from src.entities.generic_entity import GenericEntity
from src.entities.user import User
from src.entities.workspace import Workspace
from src.services.generic_service import GenericService
from src.services.ports.workspace_repository import WorkspaceRepository


Entity = TypeVar('Entity', bound=GenericEntity)


class GenericEntityService(GenericService[Entity], metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def get_workspace_repository(self) -> WorkspaceRepository:
        raise NotImplementedError

    @abc.abstractmethod
    def pre_persist_custom(self, entity: Entity, is_create: bool):
        raise NotImplementedError

    def pre_persist(self, entity: Entity, is_create: bool):
        current_user = self.get_authentication_repository().get_current_user()
        workspace: Workspace = self.get_workspace_repository().find_by_id(entity.workspace.id)
        entity.workspace = workspace

        if not workspace.user_has_permission(current_user):
            raise PermissionException(current_user)

        if not is_create:
            old_entity = self.find_by_id(entity.id)
            entity.update_original_fields(old_entity)

            if entity.workspace != old_entity.workspace:
                raise InvalidEntityException(self._get_entity_type_name(), ["workspace"])

        entity.update_audit_fields(current_user, is_create=is_create)

        self.pre_persist_custom(entity, is_create=is_create)

    def check_read_permission(self, entity: Entity, current_user: User):
        if not entity.workspace.user_has_permission(current_user):
            raise PermissionException(current_user)
