import abc
from typing import TypeVar, List
from uuid import UUID

from src.entities.exceptions.entity_not_found_exception import EntityNotFoundException
from src.entities.exceptions.invalid_entity_exception import InvalidEntityException
from src.entities.exceptions.permission_exception import PermissionException
from src.entities.generic_entity import GenericEntity
from src.entities.user import User
from src.entities.workspace import Workspace
from src.services.generic_service import GenericService
from src.services.ports.generic_entity_repository import GenericEntityRepository
from src.services.workspace_service import WorkspaceService

Entity = TypeVar('Entity', bound=GenericEntity)


class GenericEntityService(GenericService[Entity], metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def get_workspace_service(self) -> WorkspaceService:
        raise NotImplementedError

    @abc.abstractmethod
    def get_repository(self) -> GenericEntityRepository:
        raise NotImplementedError

    @abc.abstractmethod
    def pre_persist_custom(self, entity: Entity, is_create: bool):
        raise NotImplementedError

    def find_all(self, workspace_id: UUID) -> List[Entity]:
        workspace = self.get_workspace_service().find_by_id(workspace_id)
        entities = self.get_repository().find_all(workspace.id)
        current_user = self.get_authentication_repository().get_current_user()
        for entity in entities:
            self.check_read_permission(entity, current_user)
        return entities

    def pre_persist(self, entity: Entity, is_create: bool):
        current_user = self.get_authentication_repository().get_current_user()

        try:
            workspace: Workspace = self.get_workspace_service().find_by_id(entity.workspace.id)
        except EntityNotFoundException:
            raise InvalidEntityException(self._get_entity_type_name(), ["workspace"])

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
