from typing import Any, Optional

from pydantic import AnyHttpUrl, BaseSettings, Field, PositiveInt, validator
from pydantic.networks import EmailStr, PostgresDsn, RedisDsn

from src.core.constants import EnvironmentEnum


class Environment(BaseSettings):
    ENVIRONMENT: EnvironmentEnum

    def __str__(self) -> str:
        return self.ENVIRONMENT

    def __eq__(self, other: Any) -> bool:
        return self.ENVIRONMENT.__eq__(other)

    class Config:
        env_file: str = ".env"


ENVIRONMENT = Environment()
ENV_FILE = f".env.{ENVIRONMENT}"


class Settings(BaseSettings):
    ENVIRONMENT: EnvironmentEnum

    # Application
    VERSION: str = "0.0.0"
    APPLICATION_NAME: str
    HOST: str = "0.0.0.0"
    PORT: PositiveInt = 8000
    WORKERS: PositiveInt = 4
    BASE_PATH: str = ""
    DEBUG: bool = False
    LOG_LEVEL: str = "info"

    @validator("BASE_PATH")
    def normalize_base_path(cls, value: str) -> str:
        if value:
            return f"/{value.strip().strip('/')}"

        return ""

    # Database
    SQLALCHEMY_DB_URI: PostgresDsn
    SQLALCHEMY_CONNECTION_TIMEOUT: int = 30

    # Security
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: PositiveInt = 60
    RESET_TOKEN_EXPIRE_HOURS: PositiveInt = 8

    # AWS
    AWS_URL: AnyHttpUrl = "http://localhost:4566"
    AWS_REGION: str = "sa-east-1"

    # Services
    STORAGE_BUCKET: str = "storage"
    STORAGE_URL: AnyHttpUrl = "http://localhost:4566"
    EVENTS_BROKER_URL: Optional[str] = "http://localhost:4566"
    EMAIL_BROKER_URL: Optional[str] = "http://localhost:4566"

    # Cache
    CACHE_HOST: Optional[RedisDsn]

    # First Super user
    FIRST_SUPERUSER_NAME: str
    FIRST_SUPERUSER_EMAIL: EmailStr
    FIRST_SUPERUSER_PASSWORD: str = Field(..., min_length=5)

    class Config:
        env_file: str = ENV_FILE


settings = Settings(ENVIRONMENT=ENVIRONMENT.ENVIRONMENT)
