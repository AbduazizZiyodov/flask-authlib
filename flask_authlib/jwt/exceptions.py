from typing import Optional

from flask import jsonify


class AuthErrorException(Exception):
    def __init__(self, message: str, status: Optional[int] = 401) -> None:
        self.message = message
        self.status = status


def auth_error_handler(exception: AuthErrorException):
    return jsonify(
        {
            "success": False,
            "message": exception.message
        }
    ), exception.status
