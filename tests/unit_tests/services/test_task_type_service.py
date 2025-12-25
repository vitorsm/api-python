from unittest import TestCase
from unittest.mock import Mock

from src.entities.task_type import TaskType
from src.services.ports.authentication_repository import AuthenticationRepository
from src.services.ports.task_type_repository import TaskTypeRepository
from src.services.ports.workspace_repository import WorkspaceRepository
from src.services.task_type_service import TaskTypeService
from src.services.workspace_service import WorkspaceService
from tests.mocks import task_type_mock
from tests.unit_tests.services.generic_entity_service_test import GenericEntityServiceTest


class TestTaskTypeService(GenericEntityServiceTest, TestCase):

    def setUp(self):
        self.authentication_repository = Mock(spec=AuthenticationRepository)
        self.task_type_repository = Mock(spec=TaskTypeRepository)
        self.workspace_service = Mock(spec=WorkspaceService)

        self.service = TaskTypeService(self.task_type_repository, self.authentication_repository,
                                       self.workspace_service)

        super().setUp()

    def get_workspace_service(self) -> Mock:
        return self.workspace_service

    def get_default_entity(self) -> TaskType:
        return task_type_mock.get_default_task_type()

    def get_service(self) -> TaskTypeService:
        return self.service

    def get_repository(self) -> Mock:
        return self.task_type_repository

    def get_authentication_repository(self) -> Mock:
        return self.authentication_repository
