from flask import Blueprint, request, jsonify
from injector import Injector

from src.application.api.controllers.generic_controller import GenericController
from src.application.api.mappers.user_mapper import UserMapper
from src.entities.exceptions.invalid_entity_exception import InvalidEntityException
from src.services.user_service import UserService


class UserController(GenericController[UserService, UserMapper]):

    def __init__(self, app_injector: Injector):
        self.app_injector = app_injector
        self.controller = Blueprint("user_controller", __name__, url_prefix="/api/users")
        self.start_controller()

    def get_app_injector(self) -> Injector:
        return self.app_injector

    def get_controller(self) -> Blueprint:
        return self.controller

    def has_create_endpoint(self) -> bool:
        return False

    def create_endpoints(self):

        @self.controller.route("", methods=["POST"])
        def create_user():
            user_dto = request.get_json()
            user = UserMapper.to_entity(user_dto)

            if not user:
                raise InvalidEntityException("", ["invalid entity"])

            user_service = self.app_injector.get(UserService)
            user_service.create(user)

            return jsonify(UserMapper.to_dto(user)), 201
