from typing import Any, Dict, Union


class DatabaseError(Exception):
    detail: str = None

    def __init__(self, message: str) -> None:
        self.detail = message


class NotFoundError(Exception):
    detail: str = None

    def __init__(self, message: Union[Dict[str, Any], str]) -> None:
        self.detail = message


class DataValidationError(Exception):
    detail: str = None

    def __init__(self, message: str) -> None:
        self.detail = message
