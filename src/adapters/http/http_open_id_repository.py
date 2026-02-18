import requests

from src import config
from src.entities.exceptions.authentication_exception import AuthenticationException
from src.entities.user import User
from src.services.ports.open_id_repository import OpenIdRepository
from src.utils import encryption_utils

DEFAULT_PASSWORD = "13245"


def instantiate_user_from_google_token(token: str) -> User:
    token_payload = encryption_utils.decode_google_jwt_token(token)
    idp_name = HTTPOpenIdRepository.CLIENTS[config.WEB_GOOGLE_CLIENT_ID]["idp_name"]
    login = idp_name + "_" + token_payload.get("email")

    return User(id=None, name=token_payload.get("name"), login=login,
                password=DEFAULT_PASSWORD, email=token_payload.get("email"), photo=token_payload.get("picture"))


class HTTPOpenIdRepository(OpenIdRepository):

    CLIENTS = {
        config.WEB_GOOGLE_CLIENT_ID: {
            "id": config.WEB_GOOGLE_CLIENT_ID,
            "idp_name": "GOOGLE",
            "address": "https://oauth2.googleapis.com/token",
            "token_response_key": "id_token",
            "client_secret": config.WEB_GOOGLE_SECRET,
            "redirect_uri": config.WEB_GOOGLE_REDIRECT_URI,
            "body_parameters": lambda client, code: {
                "code": code,
                "client_id": client["id"],
                "client_secret": client["client_secret"],
                "redirect_uri": client["redirect_uri"],
                "grant_type": "authorization_code"
            },
            "instantiate_user_from_token": instantiate_user_from_google_token
        }
    }

    def get_user_from_code_open_id(self, code: str, client_id: str) -> User:
        client = HTTPOpenIdRepository.CLIENTS.get(client_id)

        if not client:
            raise AuthenticationException('', ' client id not found')

        address = client["address"]
        request_body = client["body_parameters"](client, code)

        try:
            response = requests.post(address, json=request_body)
        except Exception as e:
            print(e)
            raise AuthenticationException('', ' Third part auth error')

        if response.status_code != 200:
            raise AuthenticationException('', ' Third part auth was not authorized')

        user_token = response.json()[client["token_response_key"]]

        return client["instantiate_user_from_token"](user_token)
