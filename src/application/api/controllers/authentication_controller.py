from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from injector import Injector

from src.application.api.mappers import uuid_mapper
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
# https://accounts.google.com/o/oauth2/v2/auth?client_id=258702567914-4rtkou4irucitm6ntoifouvphnap1ll2.apps.googleusercontent.com&response_type=code&scope=openid%20email%20profile&redirect_uri=http%3A%2F%2Flocalhost%3A3000%2Fauth&state=123&nonce=1
# http://localhost:3000/auth?state=123&code=4%2F0AfrIepDx3zt7GZ_ahAuKOw33aQBnsS5ZtgbNergLyqx9WLOHwK7LFM8zVIHwhWxUTe62lw&scope=email+profile+openid+https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fuserinfo.profile+https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fuserinfo.email&authuser=0&prompt=none

        @self.controller.route('code', methods=['POST'])
        def authentication_code():
            body = request.get_json()
            user_state = uuid_mapper.to_uuid(body.get('state'))
            code = body.get('code')
            client_id = body.get('client_id')

            token = self.app_injector.get(UserService).open_id_authenticate(code, client_id, user_state)

            return {"access_token": token}, 201

    @staticmethod
    def __validate_credentials_input(data: dict):
        invalid_fields = []
        if not data.get("username"):
            invalid_fields.append("username")
        if not data.get("password"):
            invalid_fields.append("password")

        if invalid_fields:
            raise InvalidEntityException("Authentication", invalid_fields)
