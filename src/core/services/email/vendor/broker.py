from typing import Any, Dict

import inject

from ...broker.vendor import Broker
from .. import EmailClient


class BrokerEmailClient(EmailClient):
    broker: Broker = inject.attr(Broker)

    def send_email(self, email: str, template: str, environment: Dict[str, Any] = {}) -> None:
        self.broker.send_message({"email": email, "template": template, "environment": environment}, topic="email")
