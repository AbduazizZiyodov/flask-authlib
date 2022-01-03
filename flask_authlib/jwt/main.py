from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from ..settings import JwtConfig
from ..database.models import get_user_model

from .views import JWTLogin
from .views import JWTRegister
from .views import BaseJwtView

from ..utils import check_table_name
from ..utils import init_base_jwt_view


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
