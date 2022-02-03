from typing import Any
from typing import Callable
from typing import Optional

from inspect import signature

from flask import Flask
from flask import request
from flask_sqlalchemy import SQLAlchemy

from ..settings import JwtConfig
from ..database.models import get_user_model

from .views import JWTLogin
from .views import JWTRegister
from .views import BaseJwtView

from .utils import decode_jwt
from ..utils import check_table_name
from ..utils import init_base_jwt_view
from ..utils import add_create_admin_command
from ..utils import get_create_admin_function

from .exceptions import AuthErrorException
from .exceptions import auth_error_handler


class JWT:
    def __init__(
        self,
        app: Flask,
        db: SQLAlchemy,
        settings: JwtConfig = JwtConfig,
        UserModel: Optional[Any] = None
    ) -> None:
        """
        Main `JWT` object which allows you to
        add JWT authentication features.
        """
        self.app, self.db = app, db
        self.settings = settings

        self.User = get_user_model(
            self.db, self.settings.TABLENAME
        ) if UserModel is None else UserModel

        self.setup()

    def setup(self) -> None:
        if not check_table_name(
            self.db,
            self.settings.TABLENAME
        ):
            self.db.create_all()

        self.app.config["SECRET_KEY"] = self.settings.SECRET_KEY

        self.app.register_error_handler(AuthErrorException, auth_error_handler)

        func = get_create_admin_function(self.db, self.settings)
        add_create_admin_command(self.app, func)

        self.setup_url_rules()

    def setup_url_rules(self) -> None:
        init_base_jwt_view(self, BaseJwtView)

        self.app.add_url_rule(
            self.settings.REGISTER_URL,
            view_func=JWTRegister.as_view("jwt_register")
        )

        self.app.add_url_rule(
            self.settings.LOGIN_URL,
            view_func=JWTLogin.as_view("jwt_login")
        )

    def jwt_required(self, func: Callable) -> None:
        """
        Decorator for protecting API endpoints with JWT tokens.
        """
        def decorator(*args, **kwargs) -> Callable:
            authorization: str = request.headers.get("Authorization")

            if not authorization:
                raise AuthErrorException(
                    "Authorization(JWT token) not in the header"
                )

            jwt_token: str = authorization.split(" ")

            if jwt_token[0].lower() != "bearer" or len(jwt_token) != 2:
                raise AuthErrorException(
                    "Check your authorization header!!!"
                )

            jwt_token: str = jwt_token[1]
            user_data = decode_jwt(jwt_token, self.settings.SECRET_KEY)

            if signature(func).parameters.get("user") is not None:
                if self.settings.USER_INFO_IN_JWT:
                    kwargs["user"] = self.settings.user_schema(**user_data)
                else:
                    user = self.User.filter_by(
                        id=int(user_data)
                    ).first()

                    kwargs["user"] = self.settings.user_schema(
                        **user.to_dict()
                    )

            return func(*args, **kwargs)

        return decorator
