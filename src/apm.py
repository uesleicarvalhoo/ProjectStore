from elasticapm.contrib.starlette import make_apm_client

from src.core.config import settings
from src.core.constants import APM_SANITIZE_FIELDS, EnvironmentEnum

apm = make_apm_client(
    {
        "SERVICE_NAME": settings.APPLICATION_NAME,
        "SERVICE_VERSION": settings.VERSION,
        "ENVIRONMENT": settings.ENVIRONMENT,
        "SERVER_URL": settings.APM_SERVER_URL,
        "SANITIZE_FIELD_NAMES": APM_SANITIZE_FIELDS,
        "COLLECT_LOCAL_VARIABLES": "errors",
        "CAPTURE_HEADERS": "true",
        "CAPTURE_BODY": "errors",
        "USE_ELASTIC_EXCEPTHOOK": True,
        "ACTIVE": settings.ENVIRONMENT != EnvironmentEnum.testing,
    }
)
