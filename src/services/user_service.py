import datetime
from uuid import uuid4

from src.entities.exceptions.authentication_exception import AuthenticationException
from src.entities.exceptions.invalid_entity_exception import InvalidEntityException
from src.entities.exceptions.permission_exception import PermissionException
from src.entities.user import User
from src.services.generic_service import GenericService
from src.services.ports.authentication_repository import AuthenticationRepository
from src.services.ports.user_repository import UserRepository
from src.utils import encryption_utils


class UserService(GenericService[User]):

    def __init__(self, user_repository: UserRepository, authentication_repository: AuthenticationRepository):
        self.__user_repository = user_repository
        self.__authentication_repository = authentication_repository

    def get_authentication_repository(self) -> AuthenticationRepository:
        return self.__authentication_repository

    def get_repository(self) -> UserRepository:
        return self.__user_repository

    def pre_persist(self, user: User, is_create: bool):
        if user.password:
            user.password = encryption_utils.encrypt_password(user.password)

        user.updated_at = datetime.datetime.now(datetime.timezone.utc)

        if is_create:
            user.id = uuid4()
            return

        current_user = self.__authentication_repository.get_current_user()
        old_user = self.find_by_id(user.id)
        user.deleted_at = old_user.deleted_at

        if current_user != user:
            raise PermissionException(current_user)

        if current_user.login != user.login:
            raise InvalidEntityException("User", ["login"])

    def check_read_permission(self, entity: User, current_user: User):
        pass

    def authenticate(self, login: str, password: str) -> User:
        user = self.__user_repository.find_by_login(login)

        if not user or not encryption_utils.check_encrypted_password(password, user.password):
            raise AuthenticationException(login)

        return user
