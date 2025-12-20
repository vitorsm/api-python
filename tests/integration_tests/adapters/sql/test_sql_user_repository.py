from src.adapters.sql.sql_user_repository import SQLUserRepository
from tests.integration_tests.adapters.base_sql_alchemy_test import BaseSQLAlchemyTest
from tests.mocks import user_mock, FIRST_DEFAULT_ID, SECOND_DEFAULT_ID


class TestSQLUserRepository(BaseSQLAlchemyTest):

    def setUp(self):
        super().setUp()
        self.repository = SQLUserRepository(self.db_instance)

    def test_create_user(self):
        # given
        user = user_mock.get_valid_user()

        # when
        self.repository.create(user)

        # then
        persisted_user = self.repository.find_by_id(user.id)
        self.assertEqual(user.login, persisted_user.login)
        self.assertEqual(user.name, persisted_user.name)
        self.assertEqual(user.password, persisted_user.password)

    def test_update_user(self):
        # given
        user = user_mock.get_default_user()
        user.name = "new name"
        user.login = "new login"
        user.password = "new password"

        # when
        self.repository.update(user)

        # then
        persisted_user = self.repository.find_by_id(user.id)
        self.assertEqual(persisted_user.name, user.name)
        self.assertEqual(persisted_user.login, user.login)
        self.assertEqual(persisted_user.password, user.password)

    def test_find_by_id(self):
        # given
        user_id = FIRST_DEFAULT_ID

        # when
        user = self.repository.find_by_id(user_id)

        # then
        self.assertIsNotNone(user)
        self.assertEqual(user_id, user.id)
        self.assertEqual("User 1", user.name)
        self.assertEqual("user1", user.login)

    def test_delete_user(self):
        # given
        user_id = SECOND_DEFAULT_ID
        user = user_mock.get_default_user()
        user.id = user_id

        # when
        self.repository.delete(user)

        # then
        persisted_user = self.repository.find_by_id(user_id)
        self.assertIsNone(persisted_user)
