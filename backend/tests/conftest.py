from typing import Generator

import pytest
from _pytest.config import Config
from sqlmodel import Session

from src.core import controller
from src.core.config import settings
from src.core.constants import ContextEnum, EnvironmentEnum
from src.core.helpers.database import drop_database, init_database, make_session
from src.core.models.context import Context
from src.core.models.user import User


def pytest_configure(config: Config):
    if settings.ENVIRONMENT != EnvironmentEnum.testing:
        raise RuntimeError(
            f"You should run tests only in testing environment! Current environment: {settings.ENVIRONMENT.name}"
        )
    drop_database()
    init_database()


@pytest.fixture(scope="session")
def session() -> Session:
    yield next(make_session())


@pytest.fixture(scope="session")
def current_user(
    session: Session,
) -> Generator[User, None, None]:
    _fake_context = Context(
        context=ContextEnum.TEST,
        method="test",
        authenticated=True,
        user_id=None,
    )
    yield controller.user.get_by_email(session, settings.FIRST_SUPERUSER_EMAIL, context=_fake_context)


@pytest.fixture(scope="session")
def context(current_user: User) -> Generator[Context, None, None]:
    _context = Context(
        context=ContextEnum.TEST,
        method="test",
        authenticated=True,
        user_id=current_user.id,
    )

    yield _context
