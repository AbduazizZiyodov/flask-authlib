# Base exception
class ConfigError(Exception):
    def __init__(self, description):
        self.description = description