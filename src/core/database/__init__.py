from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from src.apm import apm
from src.core.config import settings

engine = create_engine(settings.SQLALCHEMY_DB_URI)

SessionLocal = sessionmaker(bind=engine, autocommit=False)


async def make_session() -> Session:
    session: Session = SessionLocal()

    try:
        yield session
        session.commit()

    except Exception as err:
        session.rollback()
        apm.capture_exception()
        raise err

    finally:
        session.close()
