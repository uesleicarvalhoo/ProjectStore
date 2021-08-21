from sqlalchemy.orm import Session

from src.apm import apm
from src.core.exceptions import DatabaseError

from . import SessionLocal


async def master_session() -> Session:
    session: Session = SessionLocal()

    try:
        yield session
        session.commit()

    except Exception as err:
        session.rollback()
        apm.capture_exception()
        DatabaseError("Erro no banco de dados: %s" % str(err))

    finally:
        session.close()


async def read_session() -> Session:
    session: Session = SessionLocal()

    try:
        yield session

    finally:
        session.close()
