from abc import ABC, abstractclassmethod

from src.core.events import EventDescription


class Streamer(ABC):
    @abstractclassmethod
    def send_event(cls, description: EventDescription, context: str, **data) -> None:
        pass
