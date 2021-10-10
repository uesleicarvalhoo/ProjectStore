from elasticsearch import Elasticsearch

from src.core.config import settings
from src.core.events import EventEnum
from src.core.helpers.logger import log_error
from src.core.models import Context, Event
from src.monitoring import capture_exception

from .. import Streamer


class ElasticStreamer(Streamer):
    client: Elasticsearch = Elasticsearch()

    @classmethod
    def send_event(cls, event_code: EventEnum, context: Context, **data) -> None:
        try:
            event = Event(event_code=event_code, context=context, data=data)

            cls.client.create(
                index=f"events-{settings.APPLICATION_NAME}",
                id=event.id,
                document=event.json(by_alias=True, exclude={"context": {"message"}}),
            )

        except Exception as exc:
            capture_exception()
            log_error(f"Some error ocurred when send events: {str(exc)}")
