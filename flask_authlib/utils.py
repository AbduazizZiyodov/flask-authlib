import json
import secrets

from typing import Union
from typing import Callable

from flask import Flask

from flask import request
from flask import redirect
from flask import Response
from flask.views import View

from flask_login import current_user
from flask_sqlalchemy import SQLAlchemy

from pydantic import BaseModel
from pydantic import ValidationError

from .settings import BaseConfig


def validate_form_request(Model: BaseModel) -> bool:
    try:
        request_body: dict = request.form.to_dict()
        Model(**request_body)
        return True
    except ValidationError:
        return False


def validate_json_request(Model: BaseModel) -> Callable:
    def decorator(f) -> Callable:
        def wrapper(*args, **kwargs) -> Union[Response, Callable]:
            request_body: dict = request.get_json()

            try:
                data = Model(**request_body)
                kwargs["data"] = data
                return f(*args, **kwargs)

            except ValidationError as e:
                error_response = {}
                for error in json.loads(e.json()):
                    field, message = error["loc"][0], error["msg"]

                    error_response[field] = message

                return error_response
        return wrapper
    return decorator


def initalize_base_view(cls, base_view: View) -> None:
    base_view.db = cls.db
    base_view.base_config = cls.base_config
    base_view.alerts = cls.alerts
    base_view.template_config = cls.template_config

    base_view.User = cls.User
    base_view.HOME_URL = base_view.base_config.HOME_URL
    base_view.LOGIN_URL = base_view.base_config.LOGIN_URL
    base_view.REGISTER_URL = base_view.base_config.REGISTER_URL
    return


def init_base_jwt_view(cls, base_view: View) -> None:
    base_view.db = cls.db
    base_view.User = cls.User
    base_view.settings = cls.settings
    base_view.app_config = cls.app.config
    return


def redirect_if_authenticated(function) -> Union[Callable, Response]:
    def wrapper(*args, **kwargs):
        if current_user.is_authenticated:
            return redirect("/")
        return function(*args, **kwargs)
    return wrapper


def check_table_name(db: SQLAlchemy, table_name: str) -> bool:
    return table_name in db.engine.table_names()


def set_flask_app_config(app: Flask, config: BaseConfig) -> None:
    app.config.update(
        SECRET_KEY=secrets.token_hex(),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        STATIC_FOLDER=config.STATIC_FOLDER_NAME
    )
