from typing import List, Union

from sqlalchemy import Column, Date, ForeignKey, String, exists
from sqlalchemy.orm import Query, Session, relationship
from sqlalchemy.sql.sqltypes import Integer

from src.core.schemas import CreateFiscalNote, GetFiscalNote

from .base import BaseModel
from .file import File


class FiscalNote(BaseModel):
    __tablename__ = "fiscal_notes"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    description = Column("description", String)
    file_id = Column("file_id", String, ForeignKey("files.bucket_key"), nullable=False)
    purchase_date = Column("purchase_date", Date, nullable=False)

    items = relationship("Item", cascade="all,delete", lazy="selectin", passive_deletes=True)
    file = relationship("File", cascade="all,delete", lazy="selectin", passive_deletes=True)

    @classmethod
    def query(cls, session: Session, schema) -> Query:
        query = session.query(cls)
        if schema.id:
            return query.filter(cls.id == schema.id)

        return query

    @classmethod
    def create(cls, session: Session, schema: CreateFiscalNote, file: File) -> "FiscalNote":
        obj = cls(**schema.dict(exclude={"image", "filename"}), file=file)

        session.add(obj)
        session.commit()
        session.refresh(obj)

        return obj

    @classmethod
    def get(cls, session: Session, fiscal_note_id: int) -> Union[None, "FiscalNote"]:
        return super().get(session, fiscal_note_id)

    @classmethod
    def get_all(cls, session: Session, schema: GetFiscalNote) -> List["FiscalNote"]:
        return super().get_all(session, schema)

    @classmethod
    def delete_by_id(cls, session: Session, fiscal_note_id: int) -> Union[None, "FiscalNote"]:
        return super().delete_by_id(session, fiscal_note_id)

    @classmethod
    def exists(cls, session: Session, file_hash: str) -> bool:
        return session.query(exists().where(cls.file_hash == file_hash)).scalar()
