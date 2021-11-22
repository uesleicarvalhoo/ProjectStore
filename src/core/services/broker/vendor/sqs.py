from typing import Any, Dict, List

import boto3

from src.core.config import settings
from src.core.helpers.logger import log_error
from src.monitoring import capture_exception

from .. import Broker


class SQSBroker(Broker):
    client = boto3.client("sqs", endpoint_url=settings.AWS_URL, region_name=settings.AWS_REGION)

    def send_message(self, message: str, topic: str) -> None:
        try:
            self.client.send_message(QueueUrl=settings.EVENTS_BROKER_URL, MessageBody=message)

        except Exception as exc:
            capture_exception()
            log_error(f"Some error ocurred when send events: {str(exc)}")

    def get_messages(self) -> List[Dict[str, Any]]:
        response = self.client.receive_message(
            QueueUrl=settings.EVENTS_BROKER_URL,
        )
        return response.get("Messages", [])

    def delete_message(self, message_id: str) -> None:
        self.client.delete_message(QueueUrl=settings.EVENTS_BROKER_URL, ReceiptHandle=message_id)
