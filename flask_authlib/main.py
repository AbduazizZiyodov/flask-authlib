import secrets

from os import path
from shutil import rmtree

from typing import List

from zipfile import ZipFile
from distutils.dir_util import copy_tree

from flask import Flask
from flask import Blueprint
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

from .views import *
from .models import get_user_model
from .utils import check_table_name
from .utils import initalize_base_view

from .settings import Alerts
from .settings import BaseConfig
from .settings import TemplateConfig


class Auth(object):
    def __init__(
        self,
        app: Flask,
        db: SQLAlchemy,
        alerts: Alerts = Alerts,
        base_config: BaseConfig = BaseConfig,
        template_config: TemplateConfig = TemplateConfig,
    ) -> None:

        self.app, self.db = app, db

        self.alerts = alerts
        self.base_config = base_config
        self.template_config = template_config

        self.User = get_user_model(self.db, self.base_config.TABLENAME)

        self.blueprint_name = self.base_config.BLUEPRINT_NAME

        self.blueprint = Blueprint(
            self.blueprint_name, __name__
        )

        self.setup()

    def setup(self) -> None:
        if not check_table_name(self.db, self.base_config.TABLENAME):
            self.db.create_all()

        self.app.config.update(
            TEMPLATES_AUTO_RELOAD=True,
            STATIC_FOLDER=self.base_config.STATIC_FOLDER__NAME,
            SECRET_KEY=secrets.token_hex()
        )

        self.create_templates()
        self.setup_flask_login()
        self.setup_url_rules()

    def setup_flask_login(self) -> None:
        self.login_manager = LoginManager(self.app)

        self.login_manager.login_view = \
            self.blueprint_name + "." + self.base_config.login["name"]

        self.login_manager.login_message_category =\
            self.base_config.LOGIN_MESSAGE_CATEGORY

        @self.login_manager.user_loader
        def load_user(user_id):
            return self.User.query.get(user_id)

    def setup_url_rules(self) -> None:

        initalize_base_view(self, BaseView)

        self.blueprint.add_url_rule(
            rule=self.base_config.LOGIN_URL,
            view_func=LoginView.as_view(self.base_config.login["name"]),
            methods=["GET", "POST"]
        )

        self.blueprint.add_url_rule(
            rule=self.base_config.REGISTER_URL,
            view_func=RegisterView.as_view(self.base_config.register["name"]),
            methods=["GET", "POST"]
        )

        self.blueprint.add_url_rule(
            rule=self.base_config.LOGOUT_URL,
            view_func=LogoutView.as_view(self.base_config.logout["name"]),
            methods=["GET", "POST"]
        )

        self.app.register_blueprint(self.blueprint)

    def create_templates(self) -> None:
        dirs: List[str] = [
            self.base_config.TEMPLATES_FOLDER_NAME,
            self.base_config.STATIC_FOLDER__NAME
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

        self.copy_dirs(dirs)

    def copy_dirs(self, dirs: List[str]) -> None:
        for dir in dirs:
            copy_tree(
                self.get_file_or_dir(dir),
                path.join(self.app.root_path, dir)
            )

    def get_file_or_dir(self, name: str) -> str:
        return path.abspath(__file__).replace("main.py", name)
