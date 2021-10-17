import os
from typing import Any, Dict

import emails
from emails.template import JinjaTemplate

from src.core.config import settings
from src.core.models import User

from .. import EmailClient


class SMTPEmailClient(EmailClient):
    def send_email(self, email: str, subject: str, template: str, environment: Dict[str, Any] = {}) -> None:
        with open(os.path.join(settings.EMAIL_TEMPLATES_DIR, template)) as f:
            template_str = f.read()

        message = emails.Message(
            subject=JinjaTemplate(subject),
            html=JinjaTemplate(template_str),
            mail_from=(settings.EMAILS_FROM_NAME, settings.EMAILS_FROM_EMAIL),
        )

        smtp_options = {"host": settings.SMTP_HOST, "port": settings.SMTP_PORT}

        if settings.SMTP_TLS:
            smtp_options["tls"] = True

        if settings.SMTP_USER:
            smtp_options["user"] = settings.SMTP_USER

        if settings.SMTP_PASSWORD:
            smtp_options["password"] = settings.SMTP_PASSWORD

        message.send(to=email, render=environment, smtp=smtp_options)

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
