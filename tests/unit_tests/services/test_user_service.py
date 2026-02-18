import unittest
import uuid
from typing import Any
from unittest.mock import Mock

import jwt

from src import config
from src.entities.exceptions.authentication_exception import AuthenticationException
from src.services.generic_service import GenericService
from src.services.ports.auth_state_repository import AuthStateRepository
from src.services.ports.authentication_repository import AuthenticationRepository
from src.services.ports.open_id_repository import OpenIdRepository
from src.services.ports.user_repository import UserRepository
from src.services.user_service import UserService
from src.utils import encryption_utils
from tests.mocks import user_mock, FIRST_DEFAULT_ID
from tests.unit_tests.services.generic_service_test import GenericServiceTest


class TestUserService(GenericServiceTest, unittest.TestCase):
    def setUp(self):
        self.authentication_repository = Mock(spec=AuthenticationRepository)
        self.user_repository = Mock(spec=UserRepository)
        self.auth_state_repository = Mock(spec=AuthStateRepository)
        self.open_id_repository = Mock(spec=OpenIdRepository)

        self.service = UserService(self.user_repository, self.authentication_repository, self.auth_state_repository,
                                   self.open_id_repository)

        self.get_authentication_repository().get_current_user.return_value = user_mock.get_default_user()

        super().setUp()

    def get_default_entity(self) -> Any:
        return user_mock.get_default_user()

    def get_service(self) -> GenericService:
        return self.service

    def get_repository(self) -> Mock:
        return self.user_repository

    def get_authentication_repository(self) -> Mock:
        return self.authentication_repository

    def test_find_by_id_without_permission(self):
        # all users can fetch user data
        pass

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

    def test_open_id_authenticate_success(self):
        # given
        code = str(uuid.uuid4())
        client_id = config.WEB_GOOGLE_CLIENT_ID
        user_state = uuid.uuid4()

        mock_user = user_mock.get_default_user()
        mock_user.id = None
        self.open_id_repository.get_user_from_code_open_id.return_value = mock_user
        self.user_repository.find_by_login.return_value = user_mock.get_default_user()

        # when
        token = self.service.open_id_authenticate(code, client_id, user_state)

        # then
        self.user_repository.create.assert_not_called()

        secret = config.API_TOKEN_SECRET
        algorithm = config.JWT_ALGORITHM

        payload = jwt.decode(token, secret, algorithms=[algorithm], headers=None)
        self.assertEqual(str(FIRST_DEFAULT_ID), payload["identity"])
        self.assertEqual(str(FIRST_DEFAULT_ID), payload["sub"])

    def test_open_id_authenticate_user_not_found(self):
        # given
        code = str(uuid.uuid4())
        client_id = config.WEB_GOOGLE_CLIENT_ID
        user_state = uuid.uuid4()

        mock_user = user_mock.get_default_user()
        mock_user.id = None
        self.open_id_repository.get_user_from_code_open_id.return_value = mock_user
        self.user_repository.find_by_login.return_value = None

        # when
        token = self.service.open_id_authenticate(code, client_id, user_state)

        # then
        self.user_repository.create.assert_called_once()

        secret = config.API_TOKEN_SECRET
        algorithm = config.JWT_ALGORITHM

        payload = jwt.decode(token, secret, algorithms=[algorithm], headers=None)
        self.assertEqual(str(mock_user.id), payload["identity"])
        self.assertEqual(str(mock_user.id), payload["sub"])



