import json

import inject

from src.core.helpers.logger import log_error, logger
from src.core.services import Broker, EmailClient
from src.monitoring import capture_exception


@inject.params(client=EmailClient, broker=Broker)
def main(client: EmailClient, broker: Broker) -> None:
    messages = []

    try:
        logger.info("Loading messages from message broker..")
        messages = broker.get_messages()

    except Exception as err:
        log_error("Some error ocurred during load events", exc_info=err)
        capture_exception()
        return

    else:
        logger.info(f"Load {len(messages)} messages")

    for message in messages:
        try:
            data = json.loads(message["Body"])
            client.send_email(**data)

        except json.JSONDecodeError as err:
            log_error("Coudn't decode message data", exc_info=err)
            capture_exception()

        except Exception as err:
            log_error("Some error ocurred on send email", exc_info=err)
            capture_exception()

        else:
            broker.delete_message(message["ReceiptHandle"])


if __name__ == "__main__":
    main()
