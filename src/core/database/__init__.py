from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.core.config import settings

engine = create_engine(settings.SQLALCHEMY_DB_URI)

SessionLocal = sessionmaker(bind=engine, autocommit=False)
