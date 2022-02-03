from typing import Any

from flask import jsonify
from flask.views import MethodView
from flask_sqlalchemy import SQLAlchemy

from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash

from ..settings import JwtConfig

from ..schemas import LoginData
from ..schemas import RegisterData

from .utils import encode_jwt
from ..utils import validate_json_request

from .exceptions import AuthErrorException


class BaseJwtView(MethodView):
    User: Any
    db: SQLAlchemy
    app_config: dict
    settings: JwtConfig


class JWTRegister(BaseJwtView):
    @validate_json_request(RegisterData)
    def post(self, data: RegisterData):
        user_by_email = self.User.query.filter_by(
            email=data.email
        ).first()

        user_by_username = self.User.query.filter_by(
            username=data.username
        ).first()

        if user_by_email:
            raise AuthErrorException(self.settings.alerts.EMAIL_ALERT, 400)

        if user_by_username:
            raise AuthErrorException(self.settings.alerts.EMAIL_ALERT, 400)

        min_password_length: str = self.settings.MIN_PASSWORD_LENGTH

        if len(data.password) < min_password_length:
            raise AuthErrorException(
                self.settings.alerts.PASSWORD_LENGTH.format(
                    min_password_length
                ),
                400
            )

        password_hash = generate_password_hash(data.password)

        user = self.User(
            email=data.email,
            username=data.username,
            password_hash=password_hash
        )

        user.insert()

        return jsonify(
            {
                "success": True,
                "message": self.settings.alerts.REGISTER_SUCCESS
            }
        ), 200


class JWTLogin(BaseJwtView):
    @validate_json_request(LoginData)
    def post(self, data: LoginData):
        user = self.User.query.filter_by(
            username=data.username
        ).first()

        if user is None:

            raise AuthErrorException(
                self.settings.alerts.LOGIN_FAIL
            )

        if check_password_hash(user.password_hash, data.password):
            
            data = self.settings.user_schema(**user.to_dict())

            return jsonify(
                {
                    "access_token": encode_jwt(data, self.settings)
                }
            ), 200

        raise AuthErrorException(
            self.settings.alerts.LOGIN_FAIL
        )


__all__ = ["BaseJwtView", "JWTRegister", "JWTLogin"]
