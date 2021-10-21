class BaseConfig:
    HOME_URL = "/"
    LOGIN_URL = "/login"
    REGISTER_URL = "/register"
    LOGOUT_URL = "/logout"

    logout = {
        "path": LOGOUT_URL,
        "name": "logout_view"
    }
    login = {
        "path": LOGIN_URL,
        "name": "login_view"
    }
    register = {
        "path": REGISTER_URL,
        "name": "register_view"
    }

    BLUEPRINT_NAME: str = "auth"
    TEMPLATE_FOLDER_NAME: str = "templates"

    LOGIN_MESSAGE_CATEGORY = "info"

    MIN_PASSWORD_LENGTH = 8
    TABLENAME = "user"


class Alerts:
    EMAIL_ALERT = "This email already taken!"
    USERNAME_ALERT = "This username already taken!"

    PASSWORD_LENGTH = "Password must be 8 characters long"

    REGISTER_SUCCESS = "Register was successfuly!"

    LOGIN_FAIL = "Email or password incorrect!"

    REGISTER_FAIL = "This email and username already taken!"

    BAD_REQUEST = "Bad request!"
    REQUIRED_FIELD = "Please fill all required fields!"


class TemplateConfig:
    LOGIN_BTN = "btn-success"
    REGISTER_BTN = "btn-warning"
    LOGIN_BTN_TEXT = "Login"
    REGISTER_BTN_TEXT = "Register"
    LOGIN_PAGE_TITLE = "Login"
    REGISTER_PAGE_TITLE = "Register"
    LOGIN_LABEL_USERNAME = "Username"
    LOGIN_LABEL_PASSWORD = "Password"
    REGISTER_LABEL_USERNAME = "Username"
    REGISTER_LABEL_PASSWORD = "Password"
    REGISTER_LABEL_EMAIL = "Email address"
