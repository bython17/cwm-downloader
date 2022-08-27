class CredentialsNotFoundError(FileNotFoundError):
    ...


class InvalidCredentialsError(ValueError):
    ...


class IncorrectUrlError(Exception):
    ...


class ElementNotFoundError(Exception):
    ...
