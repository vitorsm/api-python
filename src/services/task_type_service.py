from src.entities.exceptions.invalid_entity_exception import InvalidEntityException
from src.entities.task_type import TaskType
from src.services.generic_entity_service import GenericEntityService
from src.services.ports.authentication_repository import AuthenticationRepository
from src.services.ports.generic_repository import GenericRepository
from src.services.ports.task_type_repository import TaskTypeRepository
from src.services.workspace_service import WorkspaceService


class TaskTypeService(GenericEntityService[TaskType]):

    def __init__(self, task_type_repository: TaskTypeRepository, authentication_repository: AuthenticationRepository,
                 workspace_service: WorkspaceService):
        self.__task_type_repository = task_type_repository
        self.__authentication_repository = authentication_repository
        self.__workspace_service = workspace_service

    def get_workspace_service(self) -> WorkspaceService:
        return self.__workspace_service

    def pre_persist_custom(self, task_type: TaskType, is_create: bool):
        if task_type.parent_type:
            task_type.parent_type = self.find_by_id(task_type.parent_type.id)
            if task_type.workspace != task_type.parent_type.workspace:
                raise InvalidEntityException("TaskType", ["parent_type"])

    def get_authentication_repository(self) -> AuthenticationRepository:
        return self.__authentication_repository

    def get_repository(self) -> GenericRepository:
        return self.__task_type_repository
