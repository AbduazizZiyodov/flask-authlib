from typing import Callable

from flask import request
from flask import redirect
from flask.views import View

from flask_login import current_user

from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

from pydantic import ValidationError
from pydantic.main import ModelMetaclass


bcrypt = Bcrypt()


def validate_request_body(schema: ModelMetaclass) -> bool:
    try:
        return bool(schema.parse_obj(request.form.to_dict()))
    except ValidationError:
        return False


def initalize_base_view(cls, base_view: View) -> None:
    base_view.db = cls.db
    base_view.base_config = cls.base_config
    base_view.alerts = cls.alerts
    base_view.template_config = cls.template_config

    base_view.User = cls.User
    base_view.HOME_URL = base_view.base_config.HOME_URL
    base_view.LOGIN_URL = base_view.base_config.LOGIN_URL
    base_view.REGISTER_URL = base_view.base_config.REGISTER_URL


def is_authenticated(function) -> Callable:
    def wrapper(*args, **kwargs):
        if current_user.is_authenticated:
            return redirect("/")
        return function(*args, **kwargs)
    return wrapper


def check_table_name(db: SQLAlchemy, table_name: str) -> bool:
    return table_name in db.engine.table_names()
