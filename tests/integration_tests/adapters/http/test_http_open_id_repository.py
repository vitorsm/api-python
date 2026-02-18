import uuid
from unittest import TestCase

import responses

from src import config
from src.adapters.http.http_open_id_repository import HTTPOpenIdRepository
from src.entities.exceptions.authentication_exception import AuthenticationException
from tests.mocks import file_mock_utils, google_mock


class TestHTTPOpenIdRepository(TestCase):

    def setUp(self):
        self.repository = HTTPOpenIdRepository()

    def test_get_code_invalid_client_id(self):
        # given
        client_id = str(uuid.uuid4())
        code = str(uuid.uuid4())

        # when
        with self.assertRaises(AuthenticationException) as ex:
            self.repository.get_user_from_code_open_id(code, client_id)

        # then
        self.assertIn('client id not found', str(ex.exception))

    @responses.activate
    def test_user_from_code_success(self):
        # given
        user_email = "test@email.com"
        user_name = "User Test"

        client_id = config.WEB_GOOGLE_CLIENT_ID
        code = str(uuid.uuid4())
        address = HTTPOpenIdRepository.CLIENTS[client_id]["address"]
        google_response = google_mock.get_mock_google_token_response(user_email, user_name)

        responses.add(
            responses.POST,
            address,
            json=google_response,
            status=200
        )

        # when
        user = self.repository.get_user_from_code_open_id(code, client_id)

        # then
        self.assertEqual(user_email, user.email)
        self.assertEqual(user_name, user.name)
        self.assertEqual(f"GOOGLE_{user_email}", user.login)
