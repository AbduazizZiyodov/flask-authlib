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
    STATIC_FOLDER__NAME: str = "static"

    LOGIN_MESSAGE_CATEGORY = "info"

    TABLENAME: str = "user"
    MIN_PASSWORD_LENGTH: int = 8

    EMAIL_UNIQUE: bool = True


class Alerts:
    EMAIL_ALERT: str = "This email is already taken!"
    USERNAME_ALERT: str = "This username is already taken!"

    PASSWORD_LENGTH: str = "Password must be {length} characters long!"

    REGISTER_SUCCESS: str = "Register was successfuly!"

    LOGIN_FAIL: str = "The username or password is incorrect!"

    REGISTER_FAIL: str = "This email and username are already taken!"

    BAD_REQUEST: str = "Bad request!"
    REQUIRED_FIELD: str = "Please, fill in all required fields!"


class TemplateConfig:
    LOGIN_BTN: str = "btn-success"
    REGISTER_BTN: str = "btn-warning"
    LOGIN_BTN_TEXT: str = "Login"
    REGISTER_BTN_TEXT: str = "Register"
    LOGIN_PAGE_TITLE: str = "Login"
    REGISTER_PAGE_TITLE: str = "Register"
    LOGIN_LABEL_USERNAME: str = "Username"
    LOGIN_LABEL_PASSWORD: str = "Password"
    REGISTER_LABEL_USERNAME: str = "Username"
    REGISTER_LABEL_PASSWORD: str = "Password"
    REGISTER_LABEL_EMAIL: str = "Email address"
