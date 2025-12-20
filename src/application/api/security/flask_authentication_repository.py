from uuid import UUID

from flask_jwt_extended import get_jwt_identity

from src.entities.user import User
from src.services.ports.authentication_repository import AuthenticationRepository
from src.services.ports.user_repository import UserRepository
from src.services.user_service import UserService


class FlaskAuthenticationRepository(AuthenticationRepository):
    def __init__(self, user_repository: UserRepository):
        self.__user_repository = user_repository

    def get_current_user(self) -> User:
        user_id = UUID(get_jwt_identity())
        return self.__user_repository.find_by_id(user_id)
