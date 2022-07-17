import typing as t
from functools import wraps
from inspect import signature
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy

from .guards import Guard
from .utils import decode_jwt
from ..settings import JwtConfig
from ..utils import check_table_name
from ..database.models import get_user_model
from .views import JWTLogin, JWTRegister, BaseJwtView
from .exceptions import AuthErrorException, auth_error_handler


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

        self.UserModel = get_user_model(
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
        self.setup_url_rules()

    def setup_url_rules(self) -> None:
        BaseJwtView.configure(self)

        self.app.add_url_rule(
            self.settings.REGISTER_URL,
            view_func=JWTRegister.as_view("jwt_register")
        )

        self.app.add_url_rule(
            self.settings.LOGIN_URL,
            view_func=JWTLogin.as_view("jwt_login")
        )

    def get_jwt_token(self) -> t.Optional[str]:
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

        return jwt_token

    def get_user_data(self, jwt_token: str) -> t.Any:
        email = decode_jwt(jwt_token, self.settings.SECRET_KEY)

        user_query = self.UserModel.query.filter_by(
            email=email
        ).first()

        user = self.settings.user_schema(
            **user_query.to_dict()
        )

        return user


    def set_user(
        self, jwt_token: str,
        function: t.Callable,
        *args, **kwargs
    ) -> t.Union[tuple, dict]:
        user_data = self.get_user_data(jwt_token)

        if signature(function).parameters.get("user"):
            kwargs["user"] = user_data

        return args, kwargs, user_data

    def check_permissions(self, RouteGuard: Guard, user_data: t.Any) -> None:
        if not RouteGuard().can_activate(user_data):
            raise AuthErrorException(
                "You don't have permission!", 403
            )

    def required(self, RouteGuard: t.Optional[Guard] = None) -> t.Callable:
        """
        Decorator for protecting API endpoints with JWT tokens and Guards.
        """
        def decorator(function: t.Callable):
            @wraps(function)
            def wrapper(*args, **kwargs) -> t.Callable:
                jwt_token = self.get_jwt_token()

                args, kwargs, user_data = self.set_user(
                    jwt_token, function, *args, **kwargs
                )

                if RouteGuard:
                    self.check_permissions(
                        RouteGuard, user_data
                    )

                return function(*args, **kwargs)
            return wrapper
        return decorator
