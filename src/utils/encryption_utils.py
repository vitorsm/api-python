import base64
import json
from datetime import datetime, timedelta
from uuid import UUID

import bcrypt
import jwt

from src import config


def encrypt_password(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def check_encrypted_password(password: str, encrypted_password: str) -> bool:
    return bcrypt.checkpw(password.encode("utf-8"), encrypted_password.encode("utf-8"))


def generate_jwt_token(user_id: UUID) -> str:
    def generate_jwt_body() -> dict:
        iat = datetime.utcnow()
        exp = iat + timedelta(hours=config.HOURS_TO_EXPIRATION_TOKEN)
        nbf = iat + timedelta(seconds=config.SECONDS_TO_VALID)
        return {'exp': exp, 'iat': iat, 'nbf': nbf, 'identity': str(user_id), 'sub': str(user_id)}

    def encode_jwt() -> str:
        secret = config.API_TOKEN_SECRET
        algorithm = config.JWT_ALGORITHM
        required_claims = config.JWT_REQUIRED_CLAIMS

        payload = generate_jwt_body()
        missing_claims = list(set(required_claims) - set(payload.keys()))

        if missing_claims:
            raise RuntimeError('Payload is missing required claims: %s' % ', '.join(missing_claims))

        return jwt.encode(payload, secret, algorithm=algorithm, headers=None)

    return encode_jwt()


def decode_google_jwt_token(token: str) -> dict:
    # code extracted from
    # https://stackoverflow.com/questions/16923931/python-google-ouath-authentication-decode-and-verify-id-token
    parts = token.split(".")
    if len(parts) != 3:
        raise Exception("Incorrect id token format")

    payload = parts[1]
    padded = payload + '=' * (4 - len(payload) % 4)
    decoded = base64.b64decode(padded)
    return json.loads(decoded)
