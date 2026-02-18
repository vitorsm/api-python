import json
import os
from datetime import datetime
from uuid import UUID, uuid4

from src import config
from src.entities.exceptions.authentication_exception import AuthenticationException
from src.services.ports.auth_state_repository import AuthStateRepository


class FileAuthStateRepository(AuthStateRepository):

    AUTH_STATE_DIRECTORY = "auth_state"

    def generate_user_state(self) -> UUID:
        user_state = uuid4()
        file_path = FileAuthStateRepository.__generate_user_state_file_path(user_state)
        with open(file_path, "w") as file:
            json.dump({"timestamp": datetime.now().timestamp()}, file)

        return user_state

    def check_user_state(self, user_state: UUID):
        file_path = FileAuthStateRepository.__generate_user_state_file_path(user_state)

        if not os.path.exists(file_path):
            raise AuthenticationException('', "Invalid state")

        error_description = ''
        with open(file_path, "r") as file:
            persisted_user_state = json.load(file)

        if datetime.now().timestamp() - persisted_user_state["timestamp"] > config.SECONDS_TO_EXPIRE_USER_STATE:
            error_description = " Expired state"

        os.remove(file_path)

        if error_description:
            raise AuthenticationException('', error_description)

    @staticmethod
    def __generate_user_state_file_path(user_state: UUID) -> str:
        return os.path.join(FileAuthStateRepository.__get_or_create_auth_state_directory(), str(user_state) + ".json")

    @staticmethod
    def __get_or_create_auth_state_directory() -> str:
        directory_path = FileAuthStateRepository.__get_auth_state_directory()


        if not os.path.exists(config.TEMP_FILE_REPOSITORY_DIRECTORY):
            os.makedirs(config.TEMP_FILE_REPOSITORY_DIRECTORY, exist_ok=True)

        if not os.path.isdir(directory_path):
            os.mkdir(directory_path)

        return directory_path

    @staticmethod
    def __get_auth_state_directory() -> str:
        return os.path.join(config.TEMP_FILE_REPOSITORY_DIRECTORY, FileAuthStateRepository.AUTH_STATE_DIRECTORY)