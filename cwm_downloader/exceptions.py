""" This module provides contexual exceptions for the app. """


class CredentialsNotFoundError(FileNotFoundError):
    ...


class InvalidCredentialsError(ValueError):
    ...


class IncorrectUrlError(Exception):
    ...


class ElementNotFoundError(Exception):
    ...
