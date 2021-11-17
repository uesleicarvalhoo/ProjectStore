import sys

from elasticapm.contrib.starlette import make_apm_client

from src.core.config import settings
from src.core.constants import APM_SANITIZE_FIELDS, EnvironmentEnum
from src.core.helpers.logger import logger

monitoring_client = None

if settings.MONITORING_ENABLED and settings.ENVIRONMENT != EnvironmentEnum.testing:
    monitoring_client = make_apm_client(
        {
            "SERVICE_NAME": settings.APPLICATION_NAME,
            "SERVICE_VERSION": settings.VERSION,
            "ENVIRONMENT": settings.ENVIRONMENT,
            "SERVER_URL": settings.MONITORING_SERVER_URL,
            "SANITIZE_FIELD_NAMES": APM_SANITIZE_FIELDS,
            "COLLECT_LOCAL_VARIABLES": "errors",
            "CAPTURE_HEADERS": "true",
            "CAPTURE_BODY": "off",
        }
    )


def capture_exception(exc_info: Exception = None) -> None:
    if exc_info is None:
        exc_info = sys.exc_info()

    if not monitoring_client:
        logger.error("Unknow error", exc_info=exc_info)
        return

    monitoring_client.capture_exception(exc_info=exc_info)
