import datetime
from uuid import uuid4, UUID

from src.entities.exceptions.authentication_exception import AuthenticationException
from src.entities.exceptions.invalid_entity_exception import InvalidEntityException
from src.entities.exceptions.permission_exception import PermissionException
from src.entities.user import User
from src.services.generic_service import GenericService
from src.services.ports.auth_state_repository import AuthStateRepository
from src.services.ports.authentication_repository import AuthenticationRepository
from src.services.ports.open_id_repository import OpenIdRepository
from src.services.ports.user_repository import UserRepository
from src.utils import encryption_utils


class UserService(GenericService[User]):

    def __init__(self, user_repository: UserRepository, authentication_repository: AuthenticationRepository,
                 auth_state_repository: AuthStateRepository, open_id_repository: OpenIdRepository):
        self.__user_repository = user_repository
        self.__authentication_repository = authentication_repository
        self.__auth_state_repository = auth_state_repository
        self.__open_id_repository = open_id_repository

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

    def open_id_authenticate(self, code: str, client_id: str, user_state: UUID) -> str:
        self.__auth_state_repository.check_user_state(user_state)

        user = self.__open_id_repository.get_user_from_code_open_id(code, client_id)
        persisted_user = self.__user_repository.find_by_login(user.login)

        if not persisted_user:
            self.create(user)
            persisted_user = user

        return encryption_utils.generate_jwt_token(persisted_user.id)
