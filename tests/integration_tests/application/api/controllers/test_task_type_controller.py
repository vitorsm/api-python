from typing import List
from uuid import uuid4

from src.application.api.mappers import user_mapper
from src.application.api.mappers.task_type_mapper import TaskTypeMapper
from src.application.api.mappers.user_mapper import UserMapper
from tests.integration_tests.application.api.base_api_test import BaseAPITest
from tests.integration_tests.application.api.controllers.generic_entity_controller_test import \
    GenericEntityControllerTests
from tests.mocks import task_type_mock, FIRST_DEFAULT_ID, user_mock, SECOND_DEFAULT_ID


class TestTaskTypeController(BaseAPITest, GenericEntityControllerTests):

    def get_all_entities(self) -> List[dict]:
        dto1 = self.get_default_entity()
        dto2 = self.get_default_entity()

        dto2["id"] = str(SECOND_DEFAULT_ID)
        dto2["name"] = "Type 2"
        dto2["parent_type"] = dto1

        return [dto1, dto2]

    def get_valid_entity(self) -> dict:
        dto = TaskTypeMapper.to_dto(task_type_mock.get_valid_task_type())
        dto["workspace"] = {"id": str(FIRST_DEFAULT_ID)}
        dto["created_by"] = UserMapper.to_dto(user_mock.get_default_user())
        dto["updated_by"] = UserMapper.to_dto(user_mock.get_default_user())
        return dto

    def get_default_entity(self) -> dict:
        return TaskTypeMapper.to_dto(task_type_mock.get_default_task_type())

    def get_changed_entity(self) -> dict:
        dto = self.get_default_entity()
        dto["name"] = "new name"
        return dto

    def get_invalid_entity(self) -> List[dict]:
        dto1 = self.get_valid_entity()
        dto2 = self.get_valid_entity()

        dto1["name"] = ""
        dto2["workspace"] = {"id": str(uuid4())}

        return [dto1, dto2]

    def compare_generic_entities(self, entity1: dict, entity2: dict, compare_id: bool = False):
        self.assertEqual(entity1["name"], entity2["name"])

        if entity1.get("parent_type"):
            self.assertEqual(entity1["parent_type"].get("id"), entity2["parent_type"].get("id"))
        else:
            self.assertIsNone(entity2["parent_type"], f"{entity1['id']} - {entity2['id']}")

        if entity1.get("workspace"):
            self.assertEqual(entity1["workspace"]["id"], entity2["workspace"]["id"])
        else:
            self.assertIsNone(entity2["workspace"])

    def get_api_name(self) -> str:
        return "task-types"
