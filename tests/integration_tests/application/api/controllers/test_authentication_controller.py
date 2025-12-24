from src.application.api.errors.error_code import ErrorCode
from tests.integration_tests.application.api.base_api_test import BaseAPITest


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
