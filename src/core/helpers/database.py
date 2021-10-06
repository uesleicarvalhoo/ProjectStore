from typing import Generator

from sqlmodel import Session, SQLModel, create_engine

from src.apm import apm

from .. import controller
from ..config import settings
from ..constants import AccessLevel, ContextEnum
from ..helpers.exceptions import NotFoundError
from ..models import Context, CreateUser

engine = create_engine(settings.SQLALCHEMY_DB_URI)


def make_session() -> Generator[None, Session, None]:
    with Session(engine) as session:
        try:
            yield session
            session.commit()

        except Exception as err:
            session.rollback()
            apm.capture_exception()
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
            schema = CreateUser(
                name=settings.FIRST_SUPERUSER_NAME,
                email=settings.FIRST_SUPERUSER_EMAIL,
                password=settings.FIRST_SUPERUSER_PASSWORD,
                confirm_password=settings.FIRST_SUPERUSER_PASSWORD,
                access_level=AccessLevel.SUPER_USER,
            )
            controller.user.create(session, schema=schema, context=context)


def drop_database() -> None:
    SQLModel.metadata.drop_all(engine)
