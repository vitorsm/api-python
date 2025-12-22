import datetime

from src.entities.exceptions.entity_not_found_exception import EntityNotFoundException
from src.entities.exceptions.invalid_entity_exception import InvalidEntityException
from src.entities.exceptions.permission_exception import PermissionException
from src.entities.user import User
from src.entities.workspace import Workspace
from src.services.generic_service import GenericService
from src.services.ports.authentication_repository import AuthenticationRepository
from src.services.ports.workspace_repository import WorkspaceRepository
from src.services.user_service import UserService


class WorkspaceService(GenericService[Workspace]):

    def __init__(self, workspace_repository: WorkspaceRepository, authentication_repository: AuthenticationRepository,
                 user_service: UserService):
        self.__workspace_repository = workspace_repository
        self.__authentication_repository = authentication_repository
        self.__user_service = user_service

    def get_authentication_repository(self) -> AuthenticationRepository:
        return self.__authentication_repository

    def get_repository(self) -> WorkspaceRepository:
        return self.__workspace_repository

    def pre_persist(self, workspace: Workspace, is_create: bool):
        current_user = self.__authentication_repository.get_current_user()

        workspace.updated_at = datetime.datetime.now(datetime.timezone.utc)
        workspace.updated_by = current_user

        try:
            users = [self.__user_service.find_by_id(user_id) for user_id in workspace.users_ids]
        except EntityNotFoundException as e:
            raise InvalidEntityException("Workspace", ["users_ids"])

        workspace.users_ids = [u.id for u in users]

        if is_create:
            workspace.created_at = workspace.updated_at
            workspace.created_by = workspace.updated_by
        else:
            old_workspace = self.find_by_id(workspace.id)
            workspace.deleted_at = old_workspace.deleted_at
            workspace.created_at = old_workspace.created_at
            workspace.created_by = old_workspace.created_by

            if current_user != workspace.created_by:
                raise PermissionException(current_user)

    def check_read_permission(self, workspace: Workspace, current_user: User):
        if not workspace.user_has_permission(current_user):
            raise PermissionException(current_user)
