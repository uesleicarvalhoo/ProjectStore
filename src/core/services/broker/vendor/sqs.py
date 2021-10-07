import boto3

from src.core.config import settings
from src.core.events import EventCode
from src.core.helpers.logger import capture_exception, log_error
from src.core.models import Context, Event

from .. import Broker


class SQSBroker(Broker):
    __client = boto3.client("sqs", endpoint_url=settings.AWS_URL, region_name=settings.AWS_REGION)

    def send_event(self, event_code: EventCode, context: Context, **data) -> None:
        try:
            event = Event(event_code=event_code, context=context, data=data)

            self.__client.send_message(
                QueueUrl=settings.EVENTS_SQS_QUEUE,
                MessageBody=event.json(by_alias=True, exclude={"context": {"message"}}),
            )

        except Exception as exc:
            capture_exception()
            log_error(f"Some error ocurred when send events: {str(exc)}")
