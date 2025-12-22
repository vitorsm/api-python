
from src.adapters.sql.sql_workspace_repository import SQLWorkspaceRepository
from src.entities.workspace import Workspace
from src.services.ports.workspace_repository import WorkspaceRepository
from tests.integration_tests.adapters.base_sql_alchemy_test import BaseSQLAlchemyTest
from tests.integration_tests.adapters.sql.generic_repository_test import GenericRepositoryTest
from tests.mocks import workspace_mock, FIRST_DEFAULT_ID, SECOND_DEFAULT_ID, user_mock


class TestSQLWorkspaceRepository(BaseSQLAlchemyTest, GenericRepositoryTest):
    def setUp(self):
        super().setUp()
        self.repository = SQLWorkspaceRepository(self.db_instance)

    def get_valid_entity(self) -> Workspace:
        return workspace_mock.get_valid_workspace(created_by=user_mock.get_default_user(),
                                                  updated_by=user_mock.get_default_user())

    def get_default_entity(self) -> Workspace:
        return workspace_mock.get_default_workspace()

    def get_updated_entity(self) -> Workspace:
        workspace = self.get_default_entity()
        workspace.name = "new name"
        workspace.users_ids = [FIRST_DEFAULT_ID, SECOND_DEFAULT_ID]
        return workspace

    def get_repository(self) -> WorkspaceRepository:
        return self.repository

    def compare_entities(self, entity1: Workspace, entity2: Workspace):
        self.assertEqual(entity1.id, entity2.id)
        self.assertEqual(entity1.name, entity2.name)
        self.assertEqual(entity1.users_ids, entity2.users_ids)
        self.assertEqual(entity1.created_at, entity2.created_at)
        self.assertEqual(entity1.updated_at, entity2.updated_at)
        self.assertEqual(entity1.created_by, entity2.created_by)
        self.assertEqual(entity1.updated_by, entity2.updated_by)
