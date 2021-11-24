from typing import Any, Dict, List

from .. import Broker


class NoneBroker(Broker):
    def send_message(self, message: str, topic: str) -> None:
        pass

    def get_messages(self) -> List[Dict[str, Any]]:
        pass

    def delete_message(self, message_id: str) -> None:
        pass
