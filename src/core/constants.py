from enum import Enum, IntEnum, unique

from elasticapm.conf.constants import BASE_SANITIZE_FIELD_NAMES_UNPROCESSED

APM_SANITIZE_FIELDS = [] + BASE_SANITIZE_FIELD_NAMES_UNPROCESSED


@unique
class EnvironmentEnum(str, Enum):
    production = "prod"
    development = "dev"
    testing = "test"

    def __str__(self) -> str:
        return self.name


@unique
class ContextEnum(str, Enum):
    API: str = "api"
    WEB: str = "web"
    TEST: str = "test"
    APPLICATION: str = "application"


@unique
class OrderEnum(IntEnum):
    PENDING: int = 1
    COMPLETED: int = 2
    CANCELED: int = 3
