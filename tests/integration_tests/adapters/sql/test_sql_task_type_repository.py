from typing import List

from src.adapters.sql.sql_task_type_repository import SQLTaskTypeRepository
from src.entities.generic_entity import GenericEntity
from src.entities.task_type import TaskType
from src.services.ports.task_type_repository import TaskTypeRepository
from tests.integration_tests.adapters.base_sql_alchemy_test import BaseSQLAlchemyTest
from tests.integration_tests.adapters.sql.generic_entity_repository_test import GenericEntityRepositoryTest
from tests.mocks import task_type_mock, workspace_mock, user_mock, SECOND_DEFAULT_ID


class TestSQLTaskTypeRepository(BaseSQLAlchemyTest, GenericEntityRepositoryTest):

    def setUp(self):
        super().setUp()
        self.repository = SQLTaskTypeRepository(self.db_instance)

    def get_all_entities(self) -> List[GenericEntity]:
        entity1 = self.get_default_entity()
        entity2 = self.get_default_entity()

        entity2.id = SECOND_DEFAULT_ID
        entity2.name = "Type 2"
        entity2.parent_type = entity1

        return [entity1, entity2]

    def get_valid_entity(self) -> TaskType:
        task_type = task_type_mock.get_valid_task_type()
        task_type.workspace = workspace_mock.get_default_workspace()
        task_type.parent_type = self.get_default_entity()
        task_type.created_by = user_mock.get_default_user()
        task_type.updated_by = user_mock.get_default_user()

        return task_type

    def get_default_entity(self) -> TaskType:
        return task_type_mock.get_default_task_type()

    def get_updated_entity(self) -> TaskType:
        task_type = self.get_default_entity()
        task_type.name = "new name"
        return task_type

    def get_repository(self) -> TaskTypeRepository:
        return self.repository

    def compare_entities_custom(self, type1: TaskType, type2: TaskType):
        self.assertEqual(type1.parent_type, type2.parent_type)
