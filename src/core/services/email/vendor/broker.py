from typing import Any, Dict

import inject

from src.core.config import settings
from src.core.models import User

from ...broker.vendor import Broker
from .. import EmailClient


class BrokerEmailClient(EmailClient):
    broker: Broker = inject.attr(Broker)

    def send_email(self, email: str, subject: str, template: str, environment: Dict[str, Any] = {}) -> None:
        self.broker.send_message(
            {"email": email, "subject": subject, "template": template, "environment": environment}, topic="email"
        )

    def send_reset_password_email(self, user: User, reset_link: str) -> None:

        self.send_email(
            user.email,
            subject="Recuperação de senha",
            template="reset_password.html",
            environment={
                "project_name": settings.APPLICATION_NAME,
                "name": user.first_name,
                "email": user.email,
                "valid_hours": settings.EMAIL_RESET_TOKEN_EXPIRE_HOURS,
                "link": reset_link,
            },
        )
