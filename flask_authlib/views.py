from typing import Any

from flask import flash
from flask import request
from flask import redirect
from flask.views import View
from flask import render_template

from flask_sqlalchemy import SQLAlchemy

from flask_login import login_user
from flask_login import logout_user

from .utils import bcrypt
from .utils import is_authenticated
from .utils import validate_request_body

from .schemas import UserLoginData
from .schemas import UserRegisterData

from .settings import Alerts
from .settings import BaseConfig
from .settings import TemplateConfig


class BaseView(View):
    db: SQLAlchemy
    alerts: Alerts
    base_config: BaseConfig
    template_config: TemplateConfig

    User: Any
    HOME_URL: str
    LOGIN_URL: str
    REGISTER_URL: str

    def dispatch_request(self):
        if request.method == "GET":
            return self.get()
        if request.method == "POST":
            return self.post()

    def get(self):
        pass

    def post(self):
        pass


class LoginView(BaseView):

    @is_authenticated
    def get(self):
        return render_template(
            "login.html",
            title="Login",
            log=self.base_config.LOGIN_URL,
            reg=self.base_config.REGISTER_URL,
            template_cfg=self.template_config,
        )

    @is_authenticated
    def post(self):
        if not validate_request_body(UserLoginData):
            flash(self.alerts.BAD_REQUEST, "danger")
            return redirect(self.LOGIN_URL)

        username, password =\
            request.form["username"], request.form["password"]

        user = self.User.query.filter_by(
            username=username
        ).first()

        if user and bcrypt.check_password_hash(
                user.password_hash, password):
            login_user(user)

            return redirect(self.HOME_URL)

        flash(self.alerts.LOGIN_FAIL, "danger")

        return redirect(self.LOGIN_URL)


class RegisterView(BaseView):
    @is_authenticated
    def get(self):
        return render_template(
            "register.html",
            title="Register",
            log=self.base_config.LOGIN_URL,
            reg=self.base_config.REGISTER_URL,
            template_cfg=self.template_config
        )

    @is_authenticated
    def post(self):
        if not validate_request_body(UserRegisterData):
            flash(self.alerts.BAD_REQUEST, "danger")

            return redirect(self.REGISTER_URL)

        return self.validate_registration(
            **request.form.to_dict()
        )

    def validate_registration(self, **kwargs):
        user_by_email = self.User.query.filter_by(
            email=kwargs["email"]).first()

        user_by_username = self.User.query.filter_by(
            username=kwargs["username"]).first()

        if self.base_config.EMAIL_UNIQUE:
            if user_by_email is not None:
                flash(self.alerts.EMAIL_ALERT, "danger")
                return redirect(self.REGISTER_URL)
                
        if self.base_config.USERNAME_UNIQUE:
            if user_by_username is not None:
                flash(self.alerts.USERNAME_ALERT, "danger")
                return redirect(self.REGISTER_URL)

        if len(kwargs["password"]) < self.base_config.MIN_PASSWORD_LENGTH:
            flash(self.alerts.PASSWORD_LENGTH, "warning")
            return redirect(self.REGISTER_URL)

        return self.add_new_user(**kwargs)

    def add_new_user(self, **kwargs):
        hashed_password = bcrypt\
            .generate_password_hash(
                kwargs['password']
            ).decode("utf-8")

        self.User(
            email=kwargs["email"],
            username=kwargs["username"],
            password_hash=hashed_password
        ).insert()

        flash(self.alerts.REGISTER_SUCCESS, "success")

        return redirect(self.LOGIN_URL)


class LogoutView(BaseView):
    def dispatch_request(self):
        logout_user()
        return redirect(self.HOME_URL)


__all__ = [
    "BaseView", "LoginView", "RegisterView", "LogoutView",
]
