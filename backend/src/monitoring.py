import sys

from src.core.helpers.logger import logger


def capture_exception(exc_info: Exception = None) -> None:
    if exc_info is None:
        exc_info = sys.exc_info()

    logger.error("Unknow error", exc_info=exc_info)
