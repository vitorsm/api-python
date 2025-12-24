import abc
from typing import TypeVar, Generic, Optional, get_args
from uuid import UUID, uuid4

from src.entities.exceptions.entity_not_found_exception import EntityNotFoundException
from src.entities.user import User
from src.services.ports.authentication_repository import AuthenticationRepository
from src.services.ports.generic_repository import GenericRepository

Entity = TypeVar("Entity")


class GenericService(Generic[Entity], metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def get_authentication_repository(self) -> AuthenticationRepository:
        raise NotImplementedError

    @abc.abstractmethod
    def get_repository(self) -> GenericRepository:
        raise NotImplementedError

    @abc.abstractmethod
    def pre_persist(self, entity: Entity, is_create: bool):
        """
        This function is called before persisting the entity. It will check if the entity is consistent,
        if the user has enough permission, and fill some attributes. For example, if the entity has an attribute
        that must be persisted in the database, it will check if this attribute exists. If it is a creation, it could
        fill attributes like created_at and created_by.

        It can raise exceptions like InvalidEntityException, PermissionException, or EntityNotFoundException.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def check_read_permission(self, entity: Entity, current_user: User):
        raise NotImplementedError

    def create(self, entity: Entity):
        entity.id = uuid4()
        self.pre_persist(entity, is_create=True)

        self.get_repository().create(entity)

    def update(self, entity: Entity):
        self.pre_persist(entity, is_create=False)

        self.get_repository().update(entity)

    def delete(self, entity: Entity, is_hard_delete: bool = False):
        self.pre_persist(entity, is_create=False)

        entity.deleted_at = entity.updated_at

        if is_hard_delete:
            self.get_repository().delete(entity)
        else:
            self.get_repository().update(entity)

    def find_by_id(self, entity_id: UUID) -> Optional[Entity]:
        entity = self.get_repository().find_by_id(entity_id)

        if not entity:
            raise EntityNotFoundException(self._get_entity_type_name(), str(entity_id))

        self.check_read_permission(entity, self.get_authentication_repository().get_current_user())

        return entity

    def _get_entity_type_name(self) -> str:
        return get_args(self.__orig_bases__[0])[0].__name__
