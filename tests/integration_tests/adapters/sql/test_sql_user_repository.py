
from src.adapters.sql.sql_user_repository import SQLUserRepository
from src.entities.user import User
from src.services.ports.generic_repository import GenericRepository
from tests.integration_tests.adapters.base_sql_alchemy_test import BaseSQLAlchemyTest
from tests.integration_tests.adapters.sql.generic_repository_test import GenericRepositoryTest
from tests.mocks import user_mock


class TestSQLUserRepository(BaseSQLAlchemyTest, GenericRepositoryTest):
    def setUp(self):
        super().setUp()
        self.repository = SQLUserRepository(self.db_instance)

    def get_valid_entity(self) -> User:
        return user_mock.get_valid_user()

    def get_default_entity(self) -> User:
        return user_mock.get_default_user()

    def get_updated_entity(self) -> User:
        user = self.get_default_entity()
        user.name = "new name"
        user.password = "12345"
        return user

    def get_repository(self) -> GenericRepository:
        return self.repository

    def compare_entities(self, entity1: User, entity2: User):
        self.assertEqual(entity1.name, entity2.name)
        self.assertEqual(entity1.login, entity2.login)
        self.assertEqual(entity1.id, entity2.id)
