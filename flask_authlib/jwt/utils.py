import jwt

from typing import Union
from flask import Response

from datetime import datetime
from datetime import timedelta

from ..settings import JwtConfig
from .exceptions import AuthErrorException


def encode_jwt(user_id: int, settings: JwtConfig):
    expiration_time: int = settings.TOKEN_LIFETIME
    secret_key: str = settings.SECRET_KEY

    try:
        payload: dict = {
            "exp": datetime.utcnow() + timedelta(seconds=expiration_time),
            "iat": datetime.utcnow(),
            "sub": user_id
        }

        return jwt.encode(payload, secret_key, algorithm="HS256")

    except Exception:
        raise AuthErrorException("An error occurred!", 500)


def decode_jwt(token: str, secret_key: str) -> Union[int, Response]:
    try:
        return int(jwt.decode(token, secret_key)["sub"])
    except jwt.ExpiredSignatureError:
        raise AuthErrorException("Signature expired. Please log in again", 401)
    except jwt.InvalidTokenError:
        raise AuthErrorException("Invalid token. Please log in again.", 401)
    except Exception:
        raise AuthErrorException("Unable to parse jwt token!", 401)
