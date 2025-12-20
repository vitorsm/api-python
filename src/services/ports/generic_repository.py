import abc
from typing import TypeVar, Generic, Optional
from uuid import UUID


Entity = TypeVar("Entity")


class GenericRepository(Generic[Entity], metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def create(self, entity: Entity):
        raise NotImplementedError

    @abc.abstractmethod
    def update(self, entity: Entity):
        raise NotImplementedError

    @abc.abstractmethod
    def delete(self, entity: Entity):
        raise NotImplementedError

    @abc.abstractmethod
    def find_by_id(self, entity_id: UUID) -> Optional[Entity]:
        raise NotImplementedError
