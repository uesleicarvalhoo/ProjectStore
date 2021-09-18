from typing import List, Union

from sqlalchemy import Column, DateTime, String, exists
from sqlalchemy.orm import Query, Session

from src.utils.date import now_datetime

from ...config import settings
from ...schemas import CreateFile, CreateItem, GetFile
from .base import BaseModel


class File(BaseModel):
    __tablename__ = "files"

    bucket_key = Column("bucket_key", String, nullable=False, unique=True, primary_key=True)
    hash = Column("hash", String, nullable=False, unique=True)
    uploaded_at = Column("uploaded_at", DateTime, default=now_datetime())

    @classmethod
    def query(cls, session: Session, schema: GetFile) -> Query:
        query = session.query(cls)
        if schema.id:
            return query.filter(cls.bucket_key == schema.bucket_key)

        return query

    @classmethod
    def create(cls, session: Session, schema: CreateFile) -> "File":
        return super().create(session, schema)

    @classmethod
    def create_with_items(cls, session: Session, schema: CreateFile, items: List[CreateItem]) -> "File":
        raise NotImplementedError

    @classmethod
    def get(cls, session: Session, bucket_key: str) -> Union[None, "File"]:
        return session.query(cls).filter(cls.bucket_key == bucket_key).first()

    @classmethod
    def get_by_hash(cls, session: Session, hash: str) -> Union[None, "File"]:
        return session.query(cls).filter(cls.hash == hash).first()

    @classmethod
    def get_all(cls, session: Session, schema: GetFile) -> List["File"]:
        return super().get_all(session, schema)

    @classmethod
    def delete_by_id(cls, session: Session, bucket_key: int) -> Union[None, "File"]:
        if obj := session.query(cls).filter(cls.bucket_key == bucket_key).first():
            session.delete(obj)
            session.commit()
            return obj

        return None

    @classmethod
    def exists(cls, session: Session, hash: str) -> bool:
        return session.query(exists().where(cls.hash == hash)).scalar()

    @property
    def src_url(self) -> str:
        return f"{settings.STATIC_FILES_HOST}/{self.bucket_key}"
