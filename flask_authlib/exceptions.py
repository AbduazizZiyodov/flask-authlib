# Base exception
class ConfigError(Exception):
    def __init__(self, description):
        self.description = description

# Auth error exception        
class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code