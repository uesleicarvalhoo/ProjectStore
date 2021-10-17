from typing import Any, Dict, Union


class DatabaseError(Exception):
    detail: str = None

    def __init__(self, message: str) -> None:
        self.detail = message
        super().__init__(message)


class NotFoundError(Exception):
    detail: str = None

    def __init__(self, message: Union[Dict[str, Any], str]) -> None:
        self.detail = message
        super().__init__(message)


class InvalidCredentialError(Exception):
    detail: str = None

    def __init__(self, message: str) -> None:
        self.detail = message
        super().__init__(message)


class NotAuthorizedError(Exception):
    detail: str = None

    def __init__(self, message: str) -> None:
        self.detail = message
        super().__init__(message)


class DataValidationError(Exception):
    detail: str = None

    def __init__(self, message: str) -> None:
        self.detail = message
        super().__init__(message)
