import logging

from src.apm import apm

logger = logging.Logger("store")

_handler = logging.StreamHandler()
_formater = logging.Formatter("[%(asctime)s] %(levelname)s: %(message)s", datefmt="%d-%m-%Y %H:%M:%S")
_handler.setFormatter(_formater)

logger.addHandler(_handler)


def log_error(message: str, exc_info: Exception = None) -> None:
    logger.error(message, exc_info=exc_info)
    apm.capture_exception()
