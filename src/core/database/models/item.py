from typing import List, Union

from sqlalchemy import Boolean, Column, Float, ForeignKey, Integer, String, exists
from sqlalchemy.orm import Query, Session, relationship

from ...schemas import CreateItem, GetItem
from .base import BaseModel
from .file import File


class Item(BaseModel):
    __tablename__ = "items"

    id = Column("id", Integer, primary_key=True)
    code = Column("code", String, nullable=False)
    name = Column("name", String, nullable=False)
    fiscal_note_id = Column(
        "fiscal_note_id", Integer, ForeignKey("fiscal_notes.id", ondelete="CASCADE"), nullable=False
    )
    file_id = Column("file_id", String, ForeignKey("files.bucket_key"), nullable=True)
    avaliable = Column("avaliable", Boolean, default=True)
    buy_value = Column("buy_value", Float, nullable=False)
    sugested_sell_value = Column("sugested_sell_value", Float, nullable=False)

    fiscal_note = relationship("FiscalNote", back_populates="items", lazy="selectin", passive_deletes=True)
    file = relationship("File", cascade="all,delete", lazy="selectin", passive_deletes=True)

    @classmethod
    def query(cls, session: Session, schema: GetItem) -> Query:
        query = session.query(cls)

        if schema.id:
            return query.filter(cls.id == schema.id)

        if schema.avaliable is not None:
            return query.filter(cls.avaliable == schema.avaliable)

        return query

    @classmethod
    def create(cls, session: Session, schema: CreateItem, fiscal_note_id: int, file: File) -> "Item":
        obj = cls(**schema.dict(exclude={"image", "filename"}), fiscal_note_id=fiscal_note_id, file=file)

        session.add(obj)
        session.commit()
        session.refresh(obj)

        return obj

    @classmethod
    def get(cls, session: Session, item_id: int) -> Union[None, "Item"]:
        return super().get(session, item_id)

    @classmethod
    def get_all(cls, session: Session, schema: GetItem) -> List["Item"]:
        return super().get_all(session, schema)

    @classmethod
    def delete_by_id(cls, session: Session, item_id: int) -> Union[None, "Item"]:
        return super().delete_by_id(session, item_id)

    @classmethod
    def exists(cls, session: Session, item_id: int = None) -> bool:
        return bool(session.query(exists().where(cls.id == item_id)).scalar())
