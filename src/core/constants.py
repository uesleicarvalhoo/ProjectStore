from enum import Enum

from elasticapm.conf.constants import BASE_SANITIZE_FIELD_NAMES_UNPROCESSED

APM_SANITIZE_FIELDS = [] + BASE_SANITIZE_FIELD_NAMES_UNPROCESSED


class Environment(str, Enum):
    production = "prod"
    development = "dev"
    testing = "test"

    def __str__(self) -> str:
        return self.name
