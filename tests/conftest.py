from typing import Generator

import pytest
from _pytest.config import Config
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from src.core.config import Settings
from src.core.constants import Environment
from src.core.database.models.base import BaseModel

settings = Settings(_env_file=".env.test", ENVIRONMENT="test")
engine = create_engine(settings.SQLALCHEMY_DB_URI)
SessionLocal = sessionmaker(bind=engine, autocommit=False)


def pytest_configure(config: Config):
    if settings.ENVIRONMENT != Environment.testing:
        raise RuntimeError(
            f"You should run tests only in testing environment! Current environment: {settings.ENVIRONMENT.name}"
        )


@pytest.fixture(scope="session")
def session() -> Generator[Session, None, None]:
    BaseModel.metadata.drop_all(engine)
    BaseModel.metadata.create_all(engine)

    yield SessionLocal()
