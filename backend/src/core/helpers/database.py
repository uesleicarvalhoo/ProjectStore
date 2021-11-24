from typing import Generator

from sqlmodel import Session, SQLModel, create_engine

from src.monitoring import capture_exception

from .. import controller
from ..config import settings
from ..constants import AccessLevel, ContextEnum
from ..models import Context, CreateUser
from .exceptions import NotFoundError
from .logger import logger

engine = create_engine(
    settings.SQLALCHEMY_DB_URI, connect_args={"connect_timeout": settings.SQLALCHEMY_CONNECTION_TIMEOUT}
)


def make_session() -> Generator[None, Session, None]:
    with Session(engine) as session:
        try:
            yield session
            session.commit()

        except Exception as err:
            session.rollback()
            capture_exception()
            raise err


def init_database() -> None:
    context = Context(
        context=ContextEnum.APPLICATION,
        method="init_database",
    )

    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        try:
            controller.user.get_by_email(session, settings.FIRST_SUPERUSER_EMAIL, context=context)

        except NotFoundError:
            try:
                schema = CreateUser(
                    name=settings.FIRST_SUPERUSER_NAME,
                    email=settings.FIRST_SUPERUSER_EMAIL,
                    password=settings.FIRST_SUPERUSER_PASSWORD,
                    confirm_password=settings.FIRST_SUPERUSER_PASSWORD,
                    access_level=AccessLevel.SUPER_USER,
                )
                controller.user.create(session, schema=schema, context=context)

            except Exception:
                logger.warning("Couldn't possible create a First Superuser, maybe it alread exists?")


def drop_database() -> None:
    SQLModel.metadata.drop_all(engine)
