from src.interfaces.exceptions import AppException


class EnvVarNotDefinedException(AppException):

    def __init__(self, env_var: str):
        self.env_var = env_var

    def __str__(self) -> str:
        return f"Environment variable {self.env_var} not defined"


class ConfigFileNotFoundException(AppException):

    def __init__(self, path: str):
        self.path = path

    def __str__(self) -> str:
        return f"Config file {self.path} doesn't exists"
