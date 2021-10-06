from typing import Any

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
    VERSION: str
    APPLICATION_NAME: str = Field(...)
    HOST: str = Field("0.0.0.0")
    PORT: PositiveInt = Field(8000)
    WORKERS: PositiveInt = Field(4)
    BASE_PATH: str = Field("")
    DEBUG: bool = Field(False)
    LOG_LEVEL: str = Field("info")

    # Database
    SQLALCHEMY_DB_URI: PostgresDsn = Field(...)

    # Security
    SECRET_KEY: str = Field(...)
    ACCESS_TOKEN_EXPIRE_MINUTES: PositiveInt = Field(60)
    ACESS_TOKEN_REFRESH_MINUTES: int = Field(5)
    ACCESS_TOKEN_NAME: str = Field("access_token")
    SESSION_KEY_NAME: str = Field("session_id")

    @validator("ACCESS_TOKEN_NAME")
    def validate_access_token_name(cls, value: str) -> str:
        return value.lower().replace("-", "_")

    # Monitoring
    APM_SERVER_URL: AnyHttpUrl = Field("http://localhost:8200/")

    # AWS
    AWS_S3_URL: AnyHttpUrl = Field("http://localhost:4566")
    AWS_S3_BUCKET: str = Field("storage")
    AWS_REGION_NAME: str = "us-east-1"

    # Files
    STATIC_FILES_HOST: str = Field(...)

    # Cache
    CACHE: RedisDsn = Field(...)

    # First Super user
    FIRST_SUPERUSER_NAME: str = Field(...)
    FIRST_SUPERUSER_EMAIL: EmailStr = Field(...)
    FIRST_SUPERUSER_PASSWORD: str = Field(..., min_length=5)

    class Config:
        env_file: str = ENV_FILE


class AppSettings(BaseSettings):
    # Application
    VERSION: str
    APPLICATION_NAME: str = Field(...)
    STATIC_FILES_HOST: str = Field(...)

    @validator("APPLICATION_NAME")
    def normalize_application_name(cls, value: str) -> str:
        return value.title().replace("-", " ").replace("_", " ")

    class Config:
        env_file: str = ENV_FILE


settings = Settings(ENVIRONMENT=ENVIRONMENT.ENVIRONMENT)
