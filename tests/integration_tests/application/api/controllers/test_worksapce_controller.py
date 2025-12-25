from typing import List
from uuid import uuid4

from src.application.api.mappers.workspace_mapper import WorkspaceMapper
from tests.integration_tests.application.api.base_api_test import BaseAPITest
from tests.integration_tests.application.api.controllers.generic_controller_test import GenericControllerTest
from tests.mocks import workspace_mock, FIRST_DEFAULT_ID, SECOND_DEFAULT_ID


class TestWorkspaceController(BaseAPITest, GenericControllerTest):

    def get_valid_entity(self) -> dict:
        return WorkspaceMapper.to_dto(workspace_mock.get_valid_workspace())

    def get_default_entity(self) -> dict:
        return WorkspaceMapper.to_dto(workspace_mock.get_default_workspace())

    def get_changed_entity(self) -> dict:
        dto = self.get_default_entity()
        dto["name"] = "new name"
        dto["users_ids"] = [str(FIRST_DEFAULT_ID), str(SECOND_DEFAULT_ID)]
        return dto

    def get_invalid_entity(self) -> List[dict]:
        dto1 = self.get_valid_entity()
        dto2 = self.get_valid_entity()

        dto1["name"] = ""
        dto2["users_ids"] = [str(uuid4())]

        return [dto1, dto2]

    def get_api_name(self) -> str:
        return "workspaces"

    def compare_entities(self, entity1: dict, entity2: dict, compare_id: bool = False):
        self.assertEqual(entity1["name"], entity2["name"])
        self.assertEqual(entity1["users_ids"], entity2["users_ids"])

        if compare_id:
            self.assertEqual(entity1["id"], entity2["id"])

    def test_create_entity_without_permission(self):
        # any user can create a workspace
        pass

    def test_get_all_entities(self):
        pass

    def test_get_all_entities_without_permission(self):
        pass

    def test_get_all_entities_without_token(self):
        pass
