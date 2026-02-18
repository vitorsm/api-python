from flask import Flask
from injector import Module, Binder, singleton

from src.adapters.files.file_auth_state_repository import FileAuthStateRepository
from src.adapters.http.http_open_id_repository import HTTPOpenIdRepository
from src.adapters.sql.db_instance import DBInstance
from src.adapters.sql.sql_task_type_repository import SQLTaskTypeRepository
from src.adapters.sql.sql_user_repository import SQLUserRepository
from src.adapters.sql.sql_workspace_repository import SQLWorkspaceRepository
from src.application.api.security.flask_authentication_repository import FlaskAuthenticationRepository
from src.services.ports.auth_state_repository import AuthStateRepository
from src.services.ports.open_id_repository import OpenIdRepository
from src.services.task_type_service import TaskTypeService
from src.services.user_service import UserService
from src.services.workspace_service import WorkspaceService


class DependencyInjector(Module):
    def __init__(self, app: Flask, db_instance: DBInstance):
        self.app = app
        self.db_instance = db_instance

    def configure(self, binder: Binder):
        user_repository = SQLUserRepository(self.db_instance)
        workspace_repository = SQLWorkspaceRepository(self.db_instance)
        task_type_repository = SQLTaskTypeRepository(self.db_instance)
        auth_state_repository = FileAuthStateRepository()
        open_id_repository = HTTPOpenIdRepository()

        authentication_repository = FlaskAuthenticationRepository(user_repository)
        user_service = UserService(user_repository, authentication_repository, auth_state_repository,
                                   open_id_repository)
        workspace_service = WorkspaceService(workspace_repository, authentication_repository, user_service)
        task_type_service = TaskTypeService(task_type_repository, authentication_repository, workspace_service)

        binder.bind(UserService, to=user_service, scope=singleton)
        binder.bind(WorkspaceService, to=workspace_service, scope=singleton)
        binder.bind(TaskTypeService, to=task_type_service, scope=singleton)
        binder.bind(AuthStateRepository, to=auth_state_repository, scope=singleton)
        binder.bind(OpenIdRepository, to=open_id_repository, scope=singleton)
