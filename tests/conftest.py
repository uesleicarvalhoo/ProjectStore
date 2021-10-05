from typing import Generator
from uuid import uuid4

import pytest
from _pytest.config import Config
from sqlmodel import Session

from src.core.config import settings
from src.core.constants import ContextEnum, EnvironmentEnum
from src.core.helpers.database import init_database, make_session
from src.core.models.context import Context


def pytest_configure(config: Config):
    if settings.ENVIRONMENT != EnvironmentEnum.testing:
        raise RuntimeError(
            f"You should run tests only in testing environment! Current environment: {settings.ENVIRONMENT.name}"
        )

    init_database()


@pytest.fixture(scope="session")
def session() -> Session:
    yield next(make_session())


@pytest.fixture(scope="session")
def context() -> Generator[Context, None, None]:
    _context = Context(
        context=ContextEnum.TEST,
        method="test",
        authenticated=True,
        user_id=uuid4(),
    )

    yield _context
