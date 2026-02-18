import json
import uuid

from tests.integration_tests.application.api.base_api_test import BaseAPITest


class TestUserStateController(BaseAPITest):

    def test_generate_and_check_state(self):
        # given
        address = "/api/user/state"

        # when
        response = self.client.post(address, json={})
        state = json.loads(response.data)["state"]
        response = self.client.post(address + "/" + state, json=state)

        # then
        self.assertEqual(response.status_code, 200)

    def test_check_state_invalid(self):
        # given
        state = str(uuid.uuid4())
        address = "/api/user/state"

        # when
        response = self.client.post(address + "/" + state)

        # then
        self.assertEqual(response.status_code, 401)
