import secrets


class BaseConfig:
    HOME_URL: str = "/"
    LOGIN_URL: str = "/login"
    REGISTER_URL: str = "/register"
    LOGOUT_URL: str = "/logout"

    logout: dict = {
        "path": LOGOUT_URL,
        "name": "logout_view"
    }
    login: dict = {
        "path": LOGIN_URL,
        "name": "login_view"
    }
    register: dict = {
        "path": REGISTER_URL,
        "name": "register_view"
    }

    BLUEPRINT_NAME: str = "auth"

    TEMPLATES_FILE_NAME: str = "templates.zip"

    TEMPLATES_FOLDER_NAME: str = "templates"
    STATIC_FOLDER_NAME: str = "static"

    LOGIN_MESSAGE_CATEGORY = "info"

    TABLENAME: str = "users"
    MIN_PASSWORD_LENGTH: int = 8

    EMAIL_UNIQUE: bool = True


class Alerts:
    EMAIL_ALERT: str = "This email is already taken!"
    USERNAME_ALERT: str = "This username is already taken!"

    PASSWORD_LENGTH: str = "Password must be {length} characters long!"

    REGISTER_SUCCESS: str = "Registration was successful!"

    LOGIN_FAIL: str = "The username or password is incorrect!"

    REGISTER_FAIL: str = "This email and username are already taken!"

    BAD_REQUEST: str = "Bad request!"
    REQUIRED_FIELD: str = "Please, fill in all required fields!"


class TemplateConfig:
    USERNAME_LABEL: str = "Username"
    PASSWORD_LABEL: str = "Password"
    EMAIL_LABEL: str = "Email address"

    LOGIN_TITLE: str = "Login"
    LOGIN_BTN_TEXT: str = "Login"
    LOGIN_PRIMARY_COLOR: str = "red"

    REGISTER_TITLE: str = "Register"
    REGISTER_BTN_TEXT: str = "Register"
    REGISTER_PRIMARY_COLOR: str = "yellow"


COLORS: dict = {
    "blue": "primary",
    "violet": "secondary",
    "green": "success",
    "red": "danger",
    "yellow": "warning",
    "light-blue": "info",
    "white": "light",
    "black": "dark"
}


class JwtConfig:
    LOGIN_URL: str = "/login"
    REGISTER_URL: str = "/register"

    TABLENAME: str = "users"
    MIN_PASSWORD_LENGTH: int = 8

    TOKEN_LIFETIME: int = 60*60  # seconds
    SECRET_KEY: str = secrets.token_hex()

    alerts: Alerts = Alerts
