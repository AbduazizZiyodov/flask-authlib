import typing as t
from os import path
from shutil import rmtree
from zipfile import ZipFile
from distutils.dir_util import copy_tree

from flask import Flask
from flask import Blueprint
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

from .utils import (
    check_table_name,
    set_flask_app_config
)
from .database.models import get_user_model
from .settings import BaseConfig, Alerts, TemplateConfig
from .views import BaseView, LoginView, RegisterView, LogoutView


class AuthManager:
    def __init__(
        self,
        app: Flask,
        db: SQLAlchemy,
        UserModel: t.Optional[t.Any] = None,
        alerts: t.Optional[Alerts] = Alerts,
        base_config: t.Optional[BaseConfig] = BaseConfig,
        template_config: t.Optional[TemplateConfig] = TemplateConfig,
    ) -> None:
        self.app, self.db = app, db
        self.alerts = alerts
        self.base_config = base_config
        self.template_config = template_config

        self.UserModel = get_user_model(db, app)\
            if UserModel is None else UserModel

        self.setup()

    def setup(self) -> t.NoReturn:
        self.blueprint_name = "auth"
        self.blueprint = Blueprint(
            self.blueprint_name, __name__
        )

        if not check_table_name(
            self.db,
            self.base_config.TABLENAME
        ):
            self.db.create_all()

        set_flask_app_config(self.app, self.base_config)

        self.create_templates()
        self.setup_flask_login()
        self.setup_url_rules()

    def setup_flask_login(self) -> None:
        self.login_manager = LoginManager(self.app)

        self.login_manager.login_view = self.get_login_view_name()

        self.login_manager.login_message_category =\
            self.base_config.LOGIN_MESSAGE_CATEGORY

        @self.login_manager.user_loader
        def load_user(user_id):
            return self.UserModel.query.get(user_id)

    def setup_url_rules(self) -> None:
        BaseView.configure(self)

        self.blueprint.add_url_rule(
            rule=self.base_config.LOGIN_URL,
            view_func=LoginView.as_view("login_view")
        )

        self.blueprint.add_url_rule(
            rule=self.base_config.REGISTER_URL,
            view_func=RegisterView.as_view("register_view")
        )

        self.blueprint.add_url_rule(
            rule=self.base_config.LOGOUT_URL,
            view_func=LogoutView.as_view("logout_view")
        )

        self.app.register_blueprint(self.blueprint)

    def create_templates(self) -> None:
        dirs: t.List[str] = [
            self.base_config.TEMPLATES_FOLDER_NAME,
            self.base_config.STATIC_FOLDER_NAME
        ]

        for dir in dirs:
            dir_path: str = self.get_file_or_dir(dir)
            if path.isdir(dir_path):
                rmtree(dir_path)

        with ZipFile(
            self.get_file_or_dir("templates.zip"),
            "r"
        ) as zip_archive:
            zip_archive.extractall(self.get_file_or_dir(""))

        if self.template_config.AUTO_REPLACE_FOLDER:
            self.copy_dirs(dirs)

    def copy_dirs(self, dirs: t.List[str]) -> t.NoReturn:
        for dir in dirs:
            copy_tree(
                self.get_file_or_dir(dir),
                path.join(self.app.root_path, dir)
            )

    def get_file_or_dir(self, name: str) -> str:
        return path.abspath(__file__).replace("main.py", name)

    def get_login_view_name(self) -> str:
        return self.blueprint_name + "." + "login_view"
