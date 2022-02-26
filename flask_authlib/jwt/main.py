import typing as t
from functools import wraps
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

from .guards import Guard



class JWT:
    def __init__(
        self,
        app: Flask,
        db: SQLAlchemy,
        settings: JwtConfig = JwtConfig,
        UserModel: t.Optional[t.Any] = None
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

    def check_authorization(self) -> t.Optional[t.Union[bool, str]]:
        authorization: str = request.headers.get("Authorization")

        if not authorization:
            raise AuthErrorException(
                "Authorization(JWT token) not in the header"
            )

        jwt_token: str = authorization.split(" ")

        if jwt_token[0].lower() != "bearer" or len(jwt_token) != 2:
            raise AuthErrorException(
                "Check your authorization header."
            )
        jwt_token: str = jwt_token[1]

        return True, jwt_token

    def get_user_data(self, jwt_token: str) -> t.Any:

        user_data = decode_jwt(jwt_token, self.settings.SECRET_KEY)

        return self.load_user(user_data)

    def load_user(self, user_data: t.Any) -> t.Any:
        if self.settings.USER_INFO_IN_JWT and\
                isinstance(user_data, dict):

            user = self.settings.user_schema(**user_data)
        else:
            user_query = self.User.query.get(
                int(user_data)
            ).to_dict()

            user = self.settings.user_schema(
                user_query.to_dict()
            )

        return user

    def set_user(self, jwt_token: str, function: t.Callable, *args, **kwargs) -> t.Union[tuple, dict]:
        user_data = self.get_user_data(jwt_token)

        if signature(function).parameters.get("user") is not None:
            kwargs["user"] = user_data

        return args, kwargs, user_data

    def can_activate(self, RouteGuard: Guard, user_data: t.Any) -> None:
        if not RouteGuard().can_activate(user_data):
            raise AuthErrorException(
                "You do not have permission!", 403
            )

    def jwt_required(self, RouteGuard: t.Optional[Guard]) -> t.Callable:
        """
        Decorator for protecting API endpoints with JWT tokens and Guards.
        """
        def decorator(function: t.Callable):
            @wraps(function)
            def wrapper(*args, **kwargs) -> t.Callable:
                _, jwt_token = self.check_authorization()

                args, kwargs, user_data = self.set_user(
                    jwt_token, function, *args, **kwargs
                )

                self.can_activate(
                    RouteGuard, user_data) if RouteGuard else None

                return function(*args, **kwargs)
            return wrapper
        return decorator
