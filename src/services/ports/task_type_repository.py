import abc

from src.services.ports.generic_entity_repository import GenericEntityRepository
from src.entities.task_type import TaskType


class TaskTypeRepository(GenericEntityRepository[TaskType], metaclass=abc.ABCMeta):
    pass
