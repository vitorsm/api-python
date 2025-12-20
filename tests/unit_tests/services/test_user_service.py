import unittest
from unittest.mock import Mock
from uuid import uuid4

from src.entities.exceptions.authentication_exception import AuthenticationException
from src.entities.exceptions.entity_not_found_exception import EntityNotFoundException
from src.entities.exceptions.invalid_entity_exception import InvalidEntityException
from src.entities.exceptions.permission_exception import PermissionException
from src.services.ports.authentication_repository import AuthenticationRepository
from src.services.ports.user_repository import UserRepository
from src.services.user_service import UserService
from src.utils import encryption_utils
from tests.mocks import user_mock


class TestUserService(unittest.TestCase):
    def setUp(self):
        self.user_repository = Mock(spec=UserRepository)
        self.authentication_repository = Mock(spec=AuthenticationRepository)
        self.service = UserService(self.user_repository, self.authentication_repository)

    def test_create_user(self):
        # given
        user = user_mock.get_default_user()
        original_user_id = user.id

        # when
        self.service.create(user)

        # then
        self.assertNotEqual(original_user_id, user.id)
        self.assertIsNotNone(user.id)
        self.user_repository.create.assert_called_once_with(user)

    def test_update_user(self):
        # given
        mock_user = user_mock.get_default_user()
        updated_user = user_mock.get_default_user()
        updated_user.name = "new name"
        self.authentication_repository.get_current_user.return_value = mock_user

        # when
        self.service.update(updated_user)

        # then
        self.user_repository.update.assert_called_once_with(updated_user)

    def test_update_different_user(self):
        # given
        mock_user = user_mock.get_default_user()
        mock_user.id = uuid4()
        updated_user = user_mock.get_default_user()
        updated_user.name = "new name"
        self.authentication_repository.get_current_user.return_value = mock_user

        # when
        with self.assertRaises(PermissionException) as ex:
            self.service.update(updated_user)

        # then
        self.user_repository.update.assert_not_called()
        self.assertIn(mock_user.login, str(ex.exception))

    def test_update_user_changing_login(self):
        # given
        mock_user = user_mock.get_default_user()
        updated_user = user_mock.get_default_user()
        updated_user.login = "new login"
        self.authentication_repository.get_current_user.return_value = mock_user

        # when
        with self.assertRaises(InvalidEntityException) as ex:
            self.service.update(updated_user)

        # then
        self.user_repository.update.assert_not_called()
        self.assertIn("User", str(ex.exception))
        self.assertIn("login", str(ex.exception))

    def test_find_by_id(self):
        # given
        mock_user = user_mock.get_default_user()
        user_id = mock_user.id
        self.user_repository.find_by_id.return_value = mock_user

        # when
        user = self.service.find_by_id(user_id)

        # then
        self.assertEqual(mock_user, user)

    def test_find_by_id_not_found(self):
        # given
        mock_user = user_mock.get_default_user()
        user_id = mock_user.id
        self.user_repository.find_by_id.return_value = None

        # when
        with self.assertRaises(EntityNotFoundException) as ex:
            self.service.find_by_id(user_id)

        # then
        self.assertIn("User", str(ex.exception))
        self.assertIn(str(user_id), str(ex.exception))

    def test_authenticate(self):
        # given
        mock_user = user_mock.get_default_user()
        login = mock_user.login
        password = mock_user.password
        mock_user.password = encryption_utils.encrypt_password(password)
        self.user_repository.find_by_login.return_value = mock_user

        # when
        user = self.service.authenticate(login, password)

        # then
        self.assertEqual(mock_user, user)

    def test_authenticate_not_found(self):
        # given
        mock_user = user_mock.get_default_user()
        login = mock_user.login
        password = mock_user.password
        mock_user.password = encryption_utils.encrypt_password(password)
        self.user_repository.find_by_login.return_value = None

        # when
        with self.assertRaises(AuthenticationException) as ex:
            self.service.authenticate(login, password)

        # then
        self.assertIn(mock_user.login, str(ex.exception))

    def test_authenticate_wrong_pass(self):
        # given
        mock_user = user_mock.get_default_user()
        login = mock_user.login
        password = "wrong password"
        mock_user.password = encryption_utils.encrypt_password(mock_user.password)
        self.user_repository.find_by_login.return_value = mock_user

        # when
        with self.assertRaises(AuthenticationException) as ex:
            self.service.authenticate(login, password)

        # then
        self.assertIn(mock_user.login, str(ex.exception))
