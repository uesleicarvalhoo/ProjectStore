from abc import ABC, abstractmethod

from src.core.events import EventCode
from src.core.models import Context


class Broker(ABC):
    @abstractmethod
    def send_event(self, event_code: EventCode, context: Context, **data) -> None:
        raise NotImplementedError
