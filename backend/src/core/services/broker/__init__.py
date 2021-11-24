from abc import ABC, abstractmethod
from typing import Any, Dict, List


class Broker(ABC):
    @abstractmethod
    def send_message(self, message: str, topic: str) -> None:
        raise NotImplementedError

    @abstractmethod
    def get_messages(self) -> List[Dict[str, Any]]:
        raise NotImplementedError

    @abstractmethod
    def delete_message(self, message_id: str) -> None:
        raise NotImplementedError
