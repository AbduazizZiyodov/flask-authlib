from typing import Any
from flask import (
    flash,
    request,
    redirect,
    render_template
)
from flask.views import MethodView
from flask_sqlalchemy import SQLAlchemy
from flask_login import login_user, logout_user
from werkzeug.security import (
    check_password_hash,
    generate_password_hash
)

from .settings import *
from .utils import (
    validate_form_request,
    redirect_if_authenticated
)
from .schemas import LoginData, RegisterData


class BaseView(MethodView):
    db: SQLAlchemy

    alerts: Alerts
    base_config: BaseConfig
    template_config: TemplateConfig

    UserModel: Any
    HOME_URL: str
    LOGIN_URL: str
    REGISTER_URL: str

    TEMPLATE_NAME: str

    methods = ["GET", "POST"]

    @classmethod
    def configure(cls, manager: Any) -> None:
        attrs: list = [
            "db", "base_config", "alerts",
            "template_config", "UserModel",
            "HOME_URL", "LOGIN_URL", "REGISTER_URL"
        ]

        for attr in attrs:
            if attr.endswith("URL"):
                setattr(cls, attr, getattr(cls.base_config, attr))
            else:
                setattr(cls, attr, getattr(manager, attr))

        return

    @redirect_if_authenticated
    def get(self):
        return self.render()

    def render(self):
        password_pattern: str = ".{" + \
            str(self.base_config.MIN_PASSWORD_LENGTH) + ",}"

        return render_template(
            self.TEMPLATE_NAME,
            title=self.get_title(),
            login_url=self.base_config.LOGIN_URL,
            register_url=self.base_config.REGISTER_URL,
            settings=self.template_config,
            password_pattern=password_pattern,
            static_folder=self.base_config.STATIC_FOLDER_NAME,
            min_password_length=self.base_config.MIN_PASSWORD_LENGTH,
            primary_color=self.get_primary_color()
        )

    def get_title(self) -> str:
        return self.TEMPLATE_NAME.split(".")[0].title()

    def get_primary_color(self) -> str:
        color: str = getattr(
            self.template_config,
            self.TEMPLATE_NAME.replace(".html", "").upper()
            + "_PRIMARY_COLOR"
        )

        return COLORS.get(color, "primary").lower()


class LoginView(BaseView):
    TEMPLATE_NAME = "login.html"

    @redirect_if_authenticated
    def post(self):
        if not validate_form_request(LoginData):
            flash(self.alerts.BAD_REQUEST, "danger")
            return redirect(self.LOGIN_URL)

        username, password = request.form["username"], request.form["password"]

        user = self.UserModel.query.filter_by(
            username=username
        ).first()

        if user and check_password_hash(
                user.password_hash, password):
            login_user(user)
            flash("Welcome!", "success")
            return redirect(self.HOME_URL)

        flash(self.alerts.LOGIN_FAIL, "danger")

        return redirect(self.LOGIN_URL)


class RegisterView(BaseView):
    TEMPLATE_NAME = "register.html"

    @redirect_if_authenticated
    def post(self):
        if not validate_form_request(RegisterData):
            flash(self.alerts.BAD_REQUEST, "danger")

            return redirect(self.REGISTER_URL)

        return self.validate_registration(
            **request.form.to_dict()
        )

    def validate_registration(self, **kwargs):
        user_by_email = self.UserModel.query.filter_by(
            email=kwargs["email"]).first()

        user_by_username = self.UserModel.query.filter_by(
            username=kwargs["username"]).first()

        if user_by_email is not None:
            flash(self.alerts.EMAIL_ALERT, "danger")
            return redirect(self.REGISTER_URL)

        if user_by_username is not None:
            flash(self.alerts.USERNAME_ALERT, "danger")
            return redirect(self.REGISTER_URL)

        if len(kwargs["password"]) < self.base_config.MIN_PASSWORD_LENGTH:
            flash(
                self.alerts.PASSWORD_LENGTH
                .format(
                    length=self.base_config.MIN_PASSWORD_LENGTH
                ),
                "warning"
            )
            return redirect(self.REGISTER_URL)

        return self.create_user(**kwargs)

    def create_user(self, **kwargs):
        kwargs["password"] = generate_password_hash(
            kwargs["password"]
        )

        self.UserModel(**kwargs).insert()

        flash(self.alerts.REGISTER_SUCCESS, "success")

        return redirect(self.LOGIN_URL)


class LogoutView(BaseView):
    def dispatch_request(self):
        logout_user()
        return redirect(self.HOME_URL)
