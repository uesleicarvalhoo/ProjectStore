import json

import inject

from src.core.helpers.logger import log_error, logger
from src.core.services import Broker, Streamer
from src.monitoring import capture_exception


@inject.params(streamer=Streamer, broker=Broker)
def main(streamer: Streamer, broker: Broker) -> None:
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
            data["event"] = data.pop("description")
            streamer.send_event(**data)

        except json.JSONDecodeError as err:
            log_error("Coudn't decode message data", exc_info=err)
            capture_exception()

        except Exception as err:
            log_error("Some error ocurred on publish event", exc_info=err)
            capture_exception()

        else:
            broker.delete_message(message["ReceiptHandle"])


if __name__ == "__main__":
    main()
