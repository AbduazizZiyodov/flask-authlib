def get_alerts() -> dict:
    """
    Simple function for returnning messages dict.
    msg = get_alerts()
    """
    messages = {
        "EMAIL_ALERT": "This email already taken!",
        "USERNAME_ALERT": "This username already taken!",
        "PASSWORD_LENGTH": "Password must be 8 characters long",
        "REGISTER_SUCCESS": "Auth success!",
        "LOGIN_FAIL": "Email or password incorect!"
    }

    return messages


def load_template_config() -> dict:
    """
    Function for returning template config (login form ...)
    config = load_template_config()
    p.s Based on bootstrap classes
    """
    config = {
        "LOGIN_BTN": 'btn-success',
        "REGISTER_BTN": 'btn-warning',
        'LOGIN_BTN_TEXT': 'Login',
        'REGISTER_BTN_TEXT': 'Register',
        "LOGIN_PAGE_TITLE": 'Login',
        "REGISTER_PAGE_TITLE": 'Register',
        'LOGIN_LABEL_USERNAME': 'Username',
        'LOGIN_LABEL_PASSWORD': 'Password',
        'REGISTER_LABEL_USERNAME': 'Username',
        'REGISTER_LABEL_PASSWORD': 'Password',
        'REGISTER_LABEL_EMAIL': 'Email address'
    }
    return config
