from flask import Blueprint
from injector import Injector

from src.application.api.controllers.generic_controller import GenericController
from src.application.api.mappers.workspace_mapper import WorkspaceMapper
from src.services.workspace_service import WorkspaceService


class WorkspaceController(GenericController[WorkspaceService, WorkspaceMapper]):

    def __init__(self, app_injector: Injector):
        self.app_injector = app_injector
        self.controller = Blueprint("workspace_controller", __name__, url_prefix="/api/workspaces")
        self.start_controller()

    def get_app_injector(self) -> Injector:
        return self.app_injector

    def get_controller(self) -> Blueprint:
        return self.controller

    def create_endpoints(self):
        pass
