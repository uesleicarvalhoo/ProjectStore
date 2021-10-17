from abc import ABC, abstractmethod
from typing import Any, Dict

from src.core.models import User


class EmailClient(ABC):
    @abstractmethod
    def send_email(self, email: str, subject: str, template: str, environment: Dict[str, Any] = {}) -> None:
        raise NotImplementedError

    def send_reset_password_email(self, user: User, reset_link: str) -> None:
        raise NotImplementedError
