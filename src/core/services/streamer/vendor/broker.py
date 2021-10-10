import inject

from src.core.events import EventEnum
from src.core.helpers.logger import log_error
from src.core.models import Context, Event
from src.monitoring import capture_exception

from ...broker.vendor import Broker
from .. import Streamer


class BrokerStreamer(Streamer):
    broker: Broker = inject.attr(Broker)

    @classmethod
    def send_event(cls, event_enum: EventEnum, context: Context, **data) -> None:
        event_code, event_description = event_enum.value
        try:
            event = Event(event_code=event_code, event_description=event_description, context=context, data=data)

            cls.broker.send_message(message=event.json(by_alias=True, exclude={"context": {"message"}}), topic="event")

        except Exception as exc:
            capture_exception()
            log_error(f"Some error ocurred when send events: {str(exc)}")
