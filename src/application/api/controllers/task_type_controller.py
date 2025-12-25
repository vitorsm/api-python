from flask import Blueprint
from injector import Injector

from src.application.api.controllers.generic_entity_controller import GenericEntityController
from src.application.api.mappers.task_type_mapper import TaskTypeMapper
from src.services.task_type_service import TaskTypeService


class TaskTypeController(GenericEntityController[TaskTypeService, TaskTypeMapper]):

    def __init__(self, app_injector: Injector):
        self.app_injector = app_injector
        self.controller = self.instantiate_controller()
        self.start_controller()

    def get_app_injector(self) -> Injector:
        return self.app_injector

    def get_controller(self) -> Blueprint:
        return self.controller

    def create_custom_endpoints(self):
        pass

    def get_controller_name(self) -> str:
        return "task-types"
