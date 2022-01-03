from typing import Callable

from flask import Flask
from flask import request
from flask.json import jsonify
from flask_sqlalchemy import SQLAlchemy

from werkzeug.datastructures import EnvironHeaders

from ..settings import JwtConfig
from ..database.models import get_user_model

from .views import JWTLogin
from .views import JWTRegister
from .views import BaseJwtView

from .utils import decode_jwt
from ..utils import check_table_name
from ..utils import init_base_jwt_view

from .exceptions import AuthErrorException
from .exceptions import auth_error_handler

from ..schemas import User


class JWT(object):
    def __init__(
        self,
        app: Flask,
        db: SQLAlchemy,
        settings: JwtConfig = JwtConfig
    ) -> None:
        self.app, self.db = app, db
        self.settings = settings
        self.User = get_user_model(self.db, "users")
        self.setup()

    def setup(self):
        if not check_table_name(
            self.db,
            self.settings.TABLENAME
        ):
            self.db.create_all()

        self.app.config["SECRET_KEY"] = self.settings.SECRET_KEY
        self.app.register_error_handler(AuthErrorException, auth_error_handler)
        self.setup_url_rules()

    def setup_url_rules(self):
        init_base_jwt_view(self, BaseJwtView)

        self.app.add_url_rule(
            "/register",
            view_func=JWTRegister.as_view("jwt_register")
        )

        self.app.add_url_rule(
            "/login",
            view_func=JWTLogin.as_view("jwt_login")
        )

    def jwt_required(self, f: Callable):
        def decorator(*args, **kwargs):
            headers: EnvironHeaders = request.headers
            authorization: str = headers.get("Authorization")

            if not authorization:
                raise AuthErrorException(
                    "Authorization(JWT token) not in the header")

            jwt_token: str = authorization.split(" ")

            if jwt_token[0].lower() != "bearer" or len(jwt_token) != 2:
                raise AuthErrorException(
                    "Check your authorization header!!!")
                    
            jwt_token: str = jwt_token[1]
            user_id = decode_jwt(jwt_token, self.settings.SECRET_KEY)
            user = self.User.query.filter_by(id=user_id).first()

            kwargs["user"] = User(
                id=user.id,
                username=user.username,
                email=user.email,
                password_hash=user.password_hash

            )
            return f(*args, **kwargs)
        return decorator
