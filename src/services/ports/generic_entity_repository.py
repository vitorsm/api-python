import abc
from typing import List
from uuid import UUID

from src.entities.generic_entity import GenericEntity
from src.services.ports.generic_repository import GenericRepository, Entity


class GenericEntityRepository(GenericRepository[Entity], metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def find_all(self, workspace_id: UUID) -> List[GenericEntity]:
        raise NotImplementedError
