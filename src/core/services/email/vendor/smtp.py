from typing import Any, Dict

from .. import EmailClient


class SMTPEmailClient(EmailClient):
    def send_email(self, email: str, template: str, environment: Dict[str, Any] = {}) -> None:
        print(f"Send email to: {email}, template: {template}, environment: {environment}")
