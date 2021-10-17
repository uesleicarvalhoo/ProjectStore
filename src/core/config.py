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

    # Database
    SQLALCHEMY_DB_URI: PostgresDsn
    SQLALCHEMY_CONNECTION_TIMEOUT: int = 30

    # Security
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: PositiveInt = 60
    ACESS_TOKEN_REFRESH_MINUTES: int = 5
    ACCESS_TOKEN_NAME: str = "access_token"
    SESSION_KEY_NAME: str = "session_id"

    @validator("ACCESS_TOKEN_NAME")
    def validate_access_token_name(cls, value: str) -> str:
        return value.lower().replace("-", "_")

    # Monitoring
    MONITORING_ENABLED: bool = False
    MONITORING_SERVER_URL: AnyHttpUrl = "http://localhost:8200"

    # AWS
    AWS_URL: AnyHttpUrl = "http://localhost:4566"
    AWS_REGION: str = "sa-east-1"

    # Services
    STORAGE_BUCKET: str = "storage"
    STORAGE_URL: AnyHttpUrl = "http://localhost:4566"
    STREAMER_USE_MESSAGE_BROKER: bool = False
    EMAILS_USE_MESSAGE_BROKER: bool = False
    EVENTS_BROKER_URL: Optional[str] = "http://localhost:4566"
    EMAIL_BROKER_URL: Optional[str] = "http://localhost:4566"

    # Cache
    CACHE_HOST: RedisDsn

    # First Super user
    FIRST_SUPERUSER_NAME: str
    FIRST_SUPERUSER_EMAIL: EmailStr
    FIRST_SUPERUSER_PASSWORD: str = Field(..., min_length=5)

    # Emails
    SMTP_TLS: bool = True
    SMTP_PORT: Optional[int] = None
    SMTP_HOST: Optional[str] = None
    SMTP_USER: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None
    EMAILS_FROM_EMAIL: Optional[EmailStr] = None
    EMAILS_FROM_NAME: Optional[str] = None
    EMAIL_RESET_TOKEN_EXPIRE_HOURS: int = 24
    EMAIL_TEMPLATES_DIR: str = "./src/core/services/email/templates"

    class Config:
        env_file: str = ENV_FILE


class AppSettings(BaseSettings):
    # Application
    VERSION: str
    APPLICATION_NAME: str
    STORAGE_URL: str

    @validator("APPLICATION_NAME")
    def normalize_application_name(cls, value: str) -> str:
        return value.title().replace("-", " ").replace("_", " ")

    class Config:
        env_file: str = ENV_FILE


settings = Settings(ENVIRONMENT=ENVIRONMENT.ENVIRONMENT)
