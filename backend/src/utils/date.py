from datetime import datetime

import pytz

DEFAULT_TIMEZONE = pytz.timezone("America/Sao_paulo")


def now_datetime(tz: pytz.timezone = DEFAULT_TIMEZONE) -> datetime:
    return datetime.now(tz=tz)
