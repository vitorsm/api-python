from flask import Blueprint
from injector import Injector

from src.application.api.mappers import uuid_mapper
from src.services.ports.auth_state_repository import AuthStateRepository


class UserStateController:

    def __init__(self, app_injector: Injector):
        self.app_injector = app_injector
        self.controller = Blueprint("user_state_controller", __name__, url_prefix="/api/user/state")
        self.create_endpoints()

    def get_controller(self) -> Blueprint:
        return self.controller

    def create_endpoints(self):
        @self.controller.route("", methods=["POST"])
        def post():
            user_state = self.app_injector.get(AuthStateRepository).generate_user_state()
            result = {
                "state": str(user_state)
            }

            return result, 201

        @self.controller.route("<string:user_state>", methods=["POST"])
        def check(user_state: str):
            user_state_uuid = uuid_mapper.to_uuid(user_state)
            self.app_injector.get(AuthStateRepository).check_user_state(user_state_uuid)

            return {}, 200
