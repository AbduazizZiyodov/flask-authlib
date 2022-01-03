import jwt

from typing import Any

from datetime import datetime
from datetime import timedelta

from flask import jsonify
from flask.views import MethodView
from flask_sqlalchemy import SQLAlchemy

from werkzeug.security import check_password_hash, generate_password_hash

from ..settings import JwtConfig

from ..schemas import LoginData
from ..schemas import RegisterData

from .utils import encode_jwt
from ..utils import validate_json_request


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

        error_message = "User with that {} is already exists!"

        if user_by_email:
            return jsonify({"success": False, "message": error_message.format("email")}), 400
        if user_by_username:
            return jsonify({"success": False, "message": error_message.format("username")}), 400

        min_password_length: str = self.settings.MIN_PASSWORD_LENGTH

        if len(data.password) < min_password_length:
            return jsonify(
                {
                    "success": False,
                    "message": f"Password must be {min_password_length} characters long!"
                }
            ), 400

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
                "message": "User successfully registered!"
            }
        ), 200


class JWTLogin(BaseJwtView):
    @validate_json_request(LoginData)
    def post(self, data: LoginData):
        user = self.User.query.filter_by(
            username=data.username
        ).first()

        if user is None:
            return jsonify(
                {
                    "success": False,
                    "message": "No user found with given username!"
                }
            ), 401

        if check_password_hash(user.password_hash, data.password):
            return jsonify(
                {
                    "access_token": encode_jwt(user.id, self.settings)
                }
            ), 200
        return jsonify(
            {
                "success": False,
                "message": "No user found with given username!"
            }
        ), 401


__all__ = ["BaseJwtView", "JWTRegister", "JWTLogin"]
