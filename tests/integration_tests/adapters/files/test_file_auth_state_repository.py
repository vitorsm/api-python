import unittest

from src import config
from src.adapters.files.file_auth_state_repository import FileAuthStateRepository
from src.entities.exceptions.authentication_exception import AuthenticationException


class TestFileAuthStateRepository(unittest.TestCase):

    def setUp(self):
        self.repository = FileAuthStateRepository()
        config.SECONDS_TO_EXPIRE_USER_STATE = 120

    def test_generate_user_state(self):
        # when
        state = self.repository.generate_user_state()

        # then
        self.assertIsNotNone(state)

    def test_check_user_state(self):
        # given/when
        state = self.repository.generate_user_state()

        # then
        self.repository.check_user_state(state)

        with self.assertRaises(AuthenticationException) as ex:
            self.repository.check_user_state(state)

        self.assertTrue("Invalid state" in str(ex.exception))

    def test_check_user_state_expired(self):
        # given
        config.SECONDS_TO_EXPIRE_USER_STATE = -1

        # when
        state = self.repository.generate_user_state()
        with self.assertRaises(AuthenticationException) as ex:
            self.repository.check_user_state(state)

        # then
        self.assertTrue("Expired state" in str(ex.exception))