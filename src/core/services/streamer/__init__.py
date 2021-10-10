from abc import ABC, abstractclassmethod

from src.core.events import EventEnum


class Streamer(ABC):
    @abstractclassmethod
    def send_event(cls, event_code: EventEnum, context: str, **data) -> None:
        pass
