from flask import Flask
from injector import Module, Binder, singleton

from src.adapters.sql.db_instance import DBInstance
from src.adapters.sql.sql_user_repository import SQLUserRepository
from src.adapters.sql.sql_workspace_repository import SQLWorkspaceRepository
from src.application.api.security.flask_authentication_repository import FlaskAuthenticationRepository
from src.services.user_service import UserService
from src.services.workspace_service import WorkspaceService


class DependencyInjector(Module):
    def __init__(self, app: Flask, db_instance: DBInstance):
        self.app = app
        self.db_instance = db_instance

    def configure(self, binder: Binder):
        user_repository = SQLUserRepository(self.db_instance)
        workspace_repository = SQLWorkspaceRepository(self.db_instance)

        authentication_repository = FlaskAuthenticationRepository(user_repository)
        user_service = UserService(user_repository, authentication_repository)
        workspace_service = WorkspaceService(workspace_repository, authentication_repository, user_service)

        binder.bind(UserService, to=user_service, scope=singleton)
        binder.bind(WorkspaceService, to=workspace_service, scope=singleton)
