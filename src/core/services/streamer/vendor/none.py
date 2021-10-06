from src.core.events import EventCode

from .. import Streamer


class NoneStreamer(Streamer):
    """
    Streamer que não executa nada, apenas implementa os metódos sem nenhuma ação
    conforme o design pattern: https://sourcemaking.com/design_patterns/null_object
    """

    def send_event(cls, event_code: EventCode, context: str, **data) -> None:
        pass
