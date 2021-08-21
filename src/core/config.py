from pydantic import AnyHttpUrl, BaseSettings, Field, PositiveInt

from src.core.constants import Environment as EnvironmemntEnum


class Environment(BaseSettings):
    ENVIRONMENT: EnvironmemntEnum

    def __str__(self) -> str:
        return self.ENVIRONMENT

    class Config:
        env_file: str = ".env"


class Settings(BaseSettings):
    ENVIRONMENT: EnvironmemntEnum

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
    SQLALCHEMY_DB_URI: str = Field(...)

    # Security
    SECRET_KEY: str = Field(...)
    ACCESS_TOKEN_EXPIRE_MINUTES: PositiveInt = Field(60)

    # Monitoring
    APM_SERVER_URL: AnyHttpUrl = Field("http://localhost:8200/")

    # AWS
    AWS_S3_URL: AnyHttpUrl = Field("http://localhost:4566")
    AWS_S3_BUCKET: str = Field("storage")
    AWS_REGION_NAME: str = "us-east-1"


settings = Settings(_env_file=f".env.{Environment()}", ENVIRONMENT=Environment().ENVIRONMENT)
