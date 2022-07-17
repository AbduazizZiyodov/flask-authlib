from jose import jwt
from jose import exceptions
from typing import Union

from datetime import datetime
from datetime import timedelta

from ..schemas import User
from ..settings import JwtConfig
from .exceptions import AuthErrorException


def encode_jwt(user: User, settings: JwtConfig) -> Union[bytes, None]:
    secret_key: str = settings.SECRET_KEY
    expiration_time: int = settings.TOKEN_LIFETIME

    try:
        payload: dict = {
            "exp": datetime.utcnow() + timedelta(seconds=expiration_time),
            "iat": datetime.utcnow(),
            "sub": str(user.email)
        }

        return jwt.encode(payload, secret_key, algorithm="HS256")

    except Exception as exc:
        print(exc)
        raise AuthErrorException("An error occurred!", 500)


def decode_jwt(token: str, secret_key: str) -> Union[int, User]:
    try:
        return jwt.decode(token, secret_key, algorithms=["HS256"])["sub"]
    except exceptions.ExpiredSignatureError:
        raise AuthErrorException("Token expired. Please log in again", 401)
    except exceptions.JOSEError as exc:
        print(exc)
        raise AuthErrorException("Invalid token. Please log in again.", 401)
    except Exception:
        raise AuthErrorException("Unable to parse jwt token!", 401)
