from abc import ABC, abstractmethod
from typing import Any, Dict


class EmailClient(ABC):
    @abstractmethod
    def send_email(self, email: str, template: str, environment: Dict[str, Any] = {}) -> None:
        raise NotImplementedError
