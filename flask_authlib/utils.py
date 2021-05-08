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