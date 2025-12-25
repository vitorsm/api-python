import abc
from typing import List

from tests.integration_tests.application.api.controllers.generic_controller_test import GenericControllerTest
from tests.mocks import FIRST_DEFAULT_ID, SECOND_DEFAULT_ID


class GenericEntityControllerTests(GenericControllerTest, metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def get_all_entities(self) -> List[dict]:
        raise NotImplementedError

    @abc.abstractmethod
    def compare_generic_entities(self, entity1: dict, entity2: dict, compare_id: bool = False):
        raise NotImplementedError

    def compare_entities(self, entity1: dict, entity2: dict, compare_id: bool = False):
        if compare_id:
            self.assertEqual(entity1["id"], entity2["id"])

        self.assertEqual(entity1["name"], entity2["name"])
        self.assertEqual(entity1["workspace"]["id"], entity2["workspace"]["id"])
        self.assert_users(entity1["created_by"], entity2["created_by"])
        self.assert_users(entity1["updated_by"], entity2["updated_by"])
        self.compare_generic_entities(entity1, entity2, compare_id=compare_id)

    def assert_users(self, user1: dict, user2: dict):
        if not user1:
            self.assertIsNone(user2)
        else:
            self.assertEqual(user1["id"], user2["id"])
            self.assertEqual(user1["name"], user2["name"])
            self.assertEqual(user1["login"], user2["login"])
            self.assertIsNone(user2["password"])

    def test_get_all_entities(self):
        # given
        workspace_id = str(FIRST_DEFAULT_ID)
        address = self.get_address()

        # when
        response = self.client.get(address, headers=self.get_default_headers(),
                                   query_string={"workspace_id": workspace_id})

        # then
        self.assertEqual(200, response.status_code, response.text)

        entities = self.get_all_entities()
        persisted_entities = response.json

        for entity, persisted_entity in zip(entities, persisted_entities):
            self.compare_entities(entity, persisted_entity, compare_id=True)

    def test_get_all_entities_without_permission(self):
        # given
        address = self.get_address()
        workspace_id = str(SECOND_DEFAULT_ID)

        # when
        response = self.client.get(address, headers=self.get_default_headers(with_permission=False),
                                   query_string={"workspace_id": workspace_id})

        # then
        self.assertEqual(403, response.status_code, response.text)
