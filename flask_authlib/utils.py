import json
import secrets
import typing as t
from flask import Flask
from flask.views import View
from flask import request, redirect, Response
from flask_login import current_user
from flask_sqlalchemy import SQLAlchemy
from pydantic import BaseModel, ValidationError

from .settings import BaseConfig


def validate_form_request(Model: BaseModel) -> bool:
    try:
        request_body: dict = request.form.to_dict()
        Model(**request_body)
        return True

    except ValidationError:
        return False


def validate_json_request(Model: BaseModel) -> t.Callable:
    def decorator(f) -> t.Callable:
        def wrapper(*args, **kwargs) -> t.Union[Response, t.Callable]:
            request_body: dict = request.get_json()

            if request_body is None:
                return {"message": "Empty request body"}, 400

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


def redirect_if_authenticated(function) -> t.Union[t.Callable, Response]:
    def wrapper(*args, **kwargs):
        if current_user.is_authenticated:
            return redirect("/")
        return function(*args, **kwargs)
    return wrapper


def check_table_name(db: SQLAlchemy, table_name: str) -> bool:
    return table_name in db.engine.table_names()


def set_flask_app_config(app: Flask, config: BaseConfig) -> None:
    app.config.update(
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        STATIC_FOLDER=config.STATIC_FOLDER_NAME
    )
