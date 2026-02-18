import datetime

import jwt

from src import config
from src.utils import encryption_utils
from tests.mocks import file_mock_utils


def generate_google_token(email: str, name: str) -> str:
    # this function simulate the google token but it is not the same. Google seems to use the algorithm RS256.
    # We are using HS256
    # the fields are the same as google token

    payload = {
        "iss":"https://accounts.google.com",
        "azp":"258702567914-4rtkou4irucitm6ntoifouvphnap1ll2.apps.googleusercontent.com",
        "aud":"258702567914-4rtkou4irucitm6ntoifouvphnap1ll2.apps.googleusercontent.com",
        "sub":"110881180931844162643",
        "email":email,
        "email_verified": True,
        "at_hash":"eqOSD9nz0GuT1FaScadNaQ",
        "nonce":"1",
        "name":name,
        "picture":"https://lh3.googleusercontent.com/a/ACg8ocLquKeQnlfxuXPzzmSJkJvahkEZWg0aHAHsFDKnblQpo4oY7Q=s96-c",
        "given_name":name,
        "family_name":name,
        "iat": datetime.datetime.utcnow(),
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    }

    return jwt.encode(payload, "123", algorithm=config.JWT_ALGORITHM)


def get_mock_google_token_response(email: str, name: str) -> dict:
    google_response = file_mock_utils.get_http_file_content("google_auth_response.json")
    google_response["id_token"] = generate_google_token(email, name)
    return google_response
