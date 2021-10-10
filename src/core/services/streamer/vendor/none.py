from src.core.events import EventEnum

from .. import Streamer


class NoneStreamer(Streamer):
    """
    Streamer que não executa nada, apenas implementa os metódos sem nenhuma ação
    conforme o design pattern: https://sourcemaking.com/design_patterns/null_object
    """

    def send_event(cls, event_code: EventEnum, context: str, **data) -> None:
        pass
