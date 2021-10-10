from typing import Any, Dict

from .. import EmailClient


class NoneEmailClient(EmailClient):
    def send_email(self, email: str, template: str, environment: Dict[str, Any] = {}) -> None:
        pass
