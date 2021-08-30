from abc import ABC, abstractclassmethod

from src.core.events import EventCode


class Streamer(ABC):
    @abstractclassmethod
    def send_event(cls, event_code: EventCode, context: str, **data) -> None:
        pass
