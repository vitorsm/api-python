from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from injector import Injector

from src.entities.exceptions.invalid_entity_exception import InvalidEntityException
from src.services.user_service import UserService


class AuthenticationController:
    def __init__(self, app_injector: Injector):
        self.app_injector = app_injector
        self.controller = Blueprint("authentication_controller", __name__, url_prefix="/api/authenticate")
        self.create_endpoints()

    def create_endpoints(self):
        @self.controller.route('', methods=['POST'])
        def authenticate():
            data = request.get_json()

            self.__validate_credentials_input(data)

            username = data.get('username')
            password = data.get('password')

            user_service = self.app_injector.get(UserService)
            user = user_service.authenticate(username, password)

            access_token = create_access_token(identity=str(user.id))

            return jsonify(access_token=access_token), 200

    @staticmethod
    def __validate_credentials_input(data: dict):
        invalid_fields = []
        if not data.get("username"):
            invalid_fields.append("username")
        if not data.get("password"):
            invalid_fields.append("password")

        if invalid_fields:
            raise InvalidEntityException("Authentication", invalid_fields)
