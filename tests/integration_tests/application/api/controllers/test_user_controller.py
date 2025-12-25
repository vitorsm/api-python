from typing import List

from src.application.api.errors.error_code import ErrorCode
from src.application.api.mappers.user_mapper import UserMapper
from tests.integration_tests.application.api.base_api_test import BaseAPITest
from tests.integration_tests.application.api.controllers.generic_controller_test import GenericControllerTest
from tests.mocks import user_mock


class TestUserController(BaseAPITest, GenericControllerTest):

    def setUp(self):
        super().setUp()

    def get_valid_entity(self) -> dict:
        user = user_mock.get_valid_user()
        dto = UserMapper.to_dto(user)
        dto["password"] = "12345"
        return dto

    def get_default_entity(self) -> dict:
        user = user_mock.get_default_user()
        dto = UserMapper.to_dto(user)
        dto["password"] = "12345"
        return dto

    def get_changed_entity(self) -> dict:
        dto = self.get_default_entity()
        dto["name"] = "new name"
        return dto

    def get_invalid_entity(self) -> List[dict]:
        dto1 = self.get_valid_entity()
        dto2 = self.get_changed_entity()

        dto1["name"] = ""
        dto2["login"] = ""

        return [dto1, dto2]

    def compare_entities(self, user1: dict, user2: dict, compare_id: bool = False):
        if compare_id:
            self.assertEqual(user1["id"], user2["id"])

        self.assertEqual(user1["name"], user2["name"])
        self.assertEqual(user1["login"], user2["login"])

    def get_api_name(self) -> str:
        return "users"

    def test_create_duplicate_user(self):
        # given
        address = self.get_address()
        user = self.get_default_entity()
        headers = self.get_default_headers()

        # when
        response = self.client.post(address, json=user, headers=headers)

        # then
        response_data = response.json
        self.assertEqual(400, response.status_code, response.text)
        self.assertEqual(ErrorCode.DUPLICATE_ENTITY.value, response_data["code"])
        self.assertIsNotNone(response_data["details"])

    def test_create_entity_without_token(self):
        # for user controller, the post is open because the user doesn't have an account when they are registering themselves
        pass

    def test_create_entity_without_permission(self):
        # for user controller, the post is open because the user doesn't have an account when they are registering themselves
        pass

    def test_get_entity_without_permission(self):
        # all users can get another user information. It returns only login and name
        pass

    def test_get_all_entities(self):
        # user controller doesn't have this function
        pass

    def test_get_all_entities_without_permission(self):
        # user controller doesn't have this function
        pass

    def test_get_all_entities_without_token(self):
        # user controller doesn't have this function
        pass
