from typing import Any
from unittest import TestCase
from unittest.mock import Mock

from src.entities.exceptions.entity_not_found_exception import EntityNotFoundException
from src.entities.exceptions.invalid_entity_exception import InvalidEntityException
from src.services.ports.authentication_repository import AuthenticationRepository
from src.services.ports.workspace_repository import WorkspaceRepository
from src.services.user_service import UserService
from src.services.workspace_service import WorkspaceService
from tests.mocks import workspace_mock
from tests.unit_tests.services.generic_service_test import GenericServiceTest


class TestWorkspaceService(GenericServiceTest, TestCase):

    def setUp(self):
        self.workspace_repository = Mock(spec_set=WorkspaceRepository)
        self.authentication_repository = Mock(spec_set=AuthenticationRepository)
        self.user_service = Mock(spec_set=UserService)
        self.service = WorkspaceService(self.workspace_repository, self.authentication_repository, self.user_service)

        super().setUp()

    def get_default_entity(self) -> Any:
        return workspace_mock.get_default_workspace()

    def get_service(self) -> WorkspaceService:
        return self.service

    def get_repository(self) -> Mock:
        return self.workspace_repository

    def get_authentication_repository(self) -> Mock:
        return self.authentication_repository

    def test_create_workspace_with_invalid_users(self):
        # given
        entity = self.get_default_entity()
        original_entity_id = entity.id
        self.user_service.find_by_id.side_effect = EntityNotFoundException("User", "id")

        # when
        with self.assertRaises(InvalidEntityException) as ex:
            self.get_service().create(entity)

        # then
        self.assertIn("users_ids", str(ex.exception))
        self.get_repository().create.assert_not_called()
