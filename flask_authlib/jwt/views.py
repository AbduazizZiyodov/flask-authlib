from typing import Any
from flask import jsonify
from flask.views import MethodView
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import (
    check_password_hash,
    generate_password_hash
)

from .utils import encode_jwt
from ..settings import JwtConfig
from ..utils import validate_json_request
from .exceptions import AuthErrorException
from ..schemas import LoginData, RegisterData


class BaseJwtView(MethodView):
    User: Any
    db: SQLAlchemy
    app_config: dict
    settings: JwtConfig

    @classmethod
    def configure(cls, manager: Any) -> None:
        for attr in ["db", "UserModel", "settings"]:
            setattr(cls, attr, getattr(manager, attr))

        cls.app_config = manager.app.config


class JWTRegister(BaseJwtView):
    @validate_json_request(RegisterData)
    def post(self, data: RegisterData):
        user_by_email = self.UserModel.query.filter_by(
            email=data.email
        ).first()

        user_by_username = self.UserModel.query.filter_by(
            username=data.username
        ).first()

        if user_by_email:
            raise AuthErrorException(self.settings.alerts.EMAIL_ALERT, 400)

        if user_by_username:
            raise AuthErrorException(self.settings.alerts.USERNAME_ALERT, 400)

        if len(data.password) < (min_password_length := self.settings.MIN_PASSWORD_LENGTH):
            raise AuthErrorException(
                self.settings.alerts.PASSWORD_LENGTH.format(
                    min_password_length
                ),
                400
            )
        data.password = generate_password_hash(data.password)
        self.UserModel(**data.dict()).insert()

        return jsonify(
            success=True,
            message=self.settings.alerts.REGISTER_SUCCESS
        ), 200


class JWTLogin(BaseJwtView):
    @validate_json_request(LoginData)
    def post(self, data: LoginData):
        user = self.UserModel.query.filter_by(
            username=data.username
        ).first()

        if user is None:
            raise AuthErrorException(
                self.settings.alerts.LOGIN_FAIL
            )

        if check_password_hash(user.password, data.password):
            data = self.settings.user_schema(**user.to_dict())
            return jsonify(access_token=encode_jwt(data, self.settings)), 200

        raise AuthErrorException(self.settings.alerts.LOGIN_FAIL)


__all__ = ["BaseJwtView", "JWTRegister", "JWTLogin"]
