from os import path
from shutil import rmtree

from typing import Any
from typing import List
from typing import Optional
from typing import NoReturn

from zipfile import ZipFile
from distutils.dir_util import copy_tree

from flask import Flask
from flask import Blueprint
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

from .views import *
from .utils import check_table_name
from .utils import initalize_base_view
from .utils import set_flask_app_config
from .utils import add_create_admin_command
from .utils import get_create_admin_function
from .database.models import get_user_model

from .settings import Alerts
from .settings import BaseConfig
from .settings import TemplateConfig


class AuthManager:
    def __init__(
        self,
        app: Flask,
        db: SQLAlchemy,
        alerts: Optional[Alerts] = Alerts,
        base_config: Optional[BaseConfig] = BaseConfig,
        template_config: Optional[TemplateConfig] = TemplateConfig,
        auto_replace_folder: Optional[bool] = True,
        UserModel: Optional[Any] = None
    ) -> None:

        self.app, self.db = app, db

        self.auto_replace_folder: bool = auto_replace_folder

        self.alerts = alerts
        self.base_config = base_config
        self.template_config = template_config

        self.User = get_user_model(
            self.db, self.base_config.TABLENAME
        ) if UserModel is None else UserModel

        self.blueprint_name = self.base_config.BLUEPRINT_NAME

        self.blueprint = Blueprint(
            self.blueprint_name, __name__
        )
        self.setup()

    def setup(self) -> NoReturn:
        if not check_table_name(
            self.db,
            self.base_config.TABLENAME
        ):
            self.db.create_all()

        set_flask_app_config(self.app, self.base_config)

        func = get_create_admin_function(self.db, self.base_config)
        add_create_admin_command(self.app, func)

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
            return self.User.query.get(user_id)

    def setup_url_rules(self) -> None:

        initalize_base_view(self, BaseView)

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
        dirs: List[str] = [
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

        if self.auto_replace_folder:
            self.copy_dirs(dirs)

    def copy_dirs(self, dirs: List[str]) -> NoReturn:
        for dir in dirs:
            copy_tree(
                self.get_file_or_dir(dir),
                path.join(self.app.root_path, dir)
            )

    def get_file_or_dir(self, name: str) -> str:
        return path.abspath(__file__).replace("main.py", name)

    def get_login_view_name(self) -> str:
        return self.blueprint_name + "." + "login_view"
