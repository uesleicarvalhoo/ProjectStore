import logging

from src.apm import apm

logging.basicConfig(level=logging.INFO, format="[%(asctime)s] %(levelname)s: %(message)s", datefmt="%d-%m-%Y %H:%M:%S")
logger = logging.getLogger(__name__)


def log_error(message: str, exc_info: Exception = None) -> None:
    logger.error(message, exc_info=exc_info)
    apm.capture_exception()
