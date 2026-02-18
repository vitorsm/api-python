from uuid import UUID

import jwt
import responses

from src import config
from src.adapters.files.file_auth_state_repository import FileAuthStateRepository
from src.adapters.http.http_open_id_repository import HTTPOpenIdRepository
from src.application.api.errors.error_code import ErrorCode
from tests.integration_tests.application.api.base_api_test import BaseAPITest
from tests.mocks import file_mock_utils, google_mock


def get_token_payload(token: str) -> dict:
    secret = config.API_TOKEN_SECRET
    algorithm = config.JWT_ALGORITHM
    return jwt.decode(token, secret, algorithms=[algorithm], headers=None)


def mock_google_idp_response(email: str, name: str) -> dict:
    # here we are mocking what google would respond
    open_id_address = HTTPOpenIdRepository.CLIENTS[config.WEB_GOOGLE_CLIENT_ID]["address"]
    google_response = google_mock.get_mock_google_token_response(email, name)
    responses.add(
        responses.POST,
        open_id_address,
        json=google_response,
        status=200
    )

def get_valid_state() -> UUID:
    state_repository = FileAuthStateRepository()
    # we need to generate this state that will be used to ensure each request is made only once
    return state_repository.generate_user_state()


class TestAuthenticationController(BaseAPITest):

    def test_authenticate(self):
        # given
        address = "/api/authenticate"
        payload = {
            "username": "user1",
            "password": "12345"
        }

        # when
        response = self.client.post(address, json=payload)

        # then
        self.assertEqual(200, response.status_code)
        self.assertIn("access_token", response.json)

    def test_authenticate_wrong_credentials(self):
        # given
        address = "/api/authenticate"
        payload = {
            "username": "user1",
            "password": "123456"
        }

        # when
        response = self.client.post(address, json=payload)

        # then
        self.assertEqual(401, response.status_code)
        response_data = response.json
        self.assertIn(ErrorCode.CREDENTIALS_ERROR.value, response_data["code"])

    def test_authenticate_wrong_credentials_invalid_user(self):
        # given
        address = "/api/authenticate"
        payload = {
            "username": "invalid",
            "password": "12345"
        }

        # when
        response = self.client.post(address, json=payload)

        # then
        self.assertEqual(401, response.status_code)
        response_data = response.json
        self.assertIn(ErrorCode.CREDENTIALS_ERROR.value, response_data["code"])

    def test_authenticate_wrong_request(self):
        # given
        address = "/api/authenticate"
        payload = {
            "test": "user1",
            "aaa": "123456"
        }

        # when
        response = self.client.post(address, json=payload)

        # then
        self.assertEqual(400, response.status_code)
        response_data = response.json
        self.assertIn(ErrorCode.VALIDATION_ERROR.value, response_data["code"])
        self.assertIn("username, password", response_data["details"])

    @responses.activate
    def test_authenticate_google_create_user(self):
        # this is a complete test that check if we are creating users correctly after a login from google
        # it will simulate the request the client will send after user authorize access in the IDP page
        # then, it will get the new user to ensure the data is correct

        # given
        user_name = "Name Test"
        user_email = "email@gmail.com"

        address = "/api/authenticate/code"
        state = get_valid_state()
        payload = {
            "state": str(state),
            "code": "123456",
            "client_id": config.WEB_GOOGLE_CLIENT_ID,
        }

        mock_google_idp_response(user_email, user_name)

        # when
        response = self.client.post(address, json=payload)

        # then
        self.assertEqual(201, response.status_code)
        token = response.json["access_token"]
        self.assertIsNotNone(token)

        payload = get_token_payload(token)
        new_user_id = payload["sub"]

        # get the user to ensure it was correctly created
        response = self.client.get(f"/api/users/{new_user_id}", headers={"Authorization": f"Bearer {token}"})
        self.assertEqual(200, response.status_code)

        user_payload = response.json
        self.assertEqual(user_name, user_payload["name"])
        self.assertEqual(user_email, user_payload["email"])
        self.assertEqual(f"GOOGLE_{user_email}", user_payload["login"])

    @responses.activate
    def test_authenticate_google_existing_user(self):
        # this is a complete test that check if we are using users correctly after a login from google
        # first it will create a user that will be used to login,
        # then, it will simulate the request the client will send after user authorize access in the IDP page

        # given
        user_name = "Name Test"
        user_email = "email@gmail.com"

        response = self.client.post("/api/users", json={
            "name": user_name,
            "email": user_email,
            "login": f"GOOGLE_{user_email}",
            "password": "12345",
        })
        user_id = response.json["id"]

        address = "/api/authenticate/code"
        state = get_valid_state()
        payload = {
            "state": str(state),
            "code": "123456",
            "client_id": config.WEB_GOOGLE_CLIENT_ID,
        }

        mock_google_idp_response(user_email, user_name)

        # when
        response = self.client.post(address, json=payload)

        # then
        self.assertEqual(201, response.status_code)
        token = response.json["access_token"]
        self.assertIsNotNone(token)

        payload = get_token_payload(token)
        new_user_id = payload["sub"]

        # checking that it is using the same user instead of creating a new one
        self.assertEqual(user_id, new_user_id)

        # checking if the token is valid
        response = self.client.get(f"/api/users/{user_id}", headers={"Authorization": f"Bearer {token}"})
        self.assertEqual(200, response.status_code)

