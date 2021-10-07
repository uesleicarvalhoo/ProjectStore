from src.core.events import EventCode
from src.core.models import Context

from .. import Broker


class NoneBroker(Broker):
    def send_event(self, event_code: EventCode, context: Context, **data) -> None:
        pass
