from typing import Generator

from sqlmodel import Session, create_engine

from src.apm import apm
from src.core.config import settings

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
