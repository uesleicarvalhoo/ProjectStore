from typing import Any, Dict

from src.core.models import User

from .. import EmailClient


class NoneEmailClient(EmailClient):
    def send_email(self, email: str, subject: str, template: str, environment: Dict[str, Any] = {}) -> None:
        pass

    def send_reset_password_email(self, user: User, reset_link: str) -> None:
        pass
