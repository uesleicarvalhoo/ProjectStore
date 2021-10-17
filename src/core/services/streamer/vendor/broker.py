import inject

from src.core.events import EventDescription
from src.core.helpers.logger import log_error
from src.core.models import Context, Event
from src.monitoring import capture_exception

from ...broker.vendor import Broker
from .. import Streamer


class BrokerStreamer(Streamer):
    broker: Broker = inject.attr(Broker)

    @classmethod
    def send_event(cls, description: EventDescription, context: Context, **data) -> None:
        try:
            event = Event(description, context=context, data=data)

            cls.broker.send_message(message=event.json(by_alias=True, exclude={"context": {"message"}}), topic="event")

        except Exception as exc:
            capture_exception()
            log_error(f"Some error ocurred when send events: {str(exc)}")
