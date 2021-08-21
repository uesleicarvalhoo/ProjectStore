from elasticsearch import Elasticsearch

from src.apm import apm
from src.core.events import EventCode
from src.core.schemas.event import Event
from src.utils.logger import log_error

from .client import Streamer


class ElasticStreamer(Streamer):
    client: Elasticsearch = Elasticsearch()

    @classmethod
    def send_event(cls, event_code: EventCode, **data) -> None:
        try:
            event = Event(event_code=event_code, data=data)

            cls.client.create(
                "events-store",
                id=event.id,
                body=event.json(by_alias=True),
            )

        except Exception as exc:
            apm.capture_exception()
            log_error(f"Some error ocurred when send events: {str(exc)}")
