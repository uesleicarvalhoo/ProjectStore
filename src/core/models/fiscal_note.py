from base64 import b64decode
from datetime import date
from typing import List, Union
from uuid import UUID, uuid4

from pydantic import validator
from sqlmodel import Column, Field, Relationship, SQLModel
from sqlmodel.sql.sqltypes import GUID

from src.monitoring import capture_exception

from .file import File
from .fiscal_note_item import CreateFiscalNoteItem, FiscalNoteItem
from .user import User


class BaseFiscalNote(SQLModel):
    description: str = Field(..., description="Description of fiscal note", min_length=1)
    purchase_date: date = Field(..., description="Date of purchase")


class CreateFiscalNote(BaseFiscalNote):
    image: bytes = Field(..., description="Content base64 of the image")
    filename: str = Field(..., description="Image filename", min_length=1)
    items: List[CreateFiscalNoteItem] = Field([], description="List of items in the fiscal note")

    @validator("image", pre=True)
    def validate_image(cls, value: Union[str, bytes]) -> bytes:
        if isinstance(value, bytes):
            return value

        try:
            return b64decode(value)

        except Exception:
            capture_exception()
            raise ValueError("Couldn't decode the file!")


class QueryFiscalNote(SQLModel):
    pass


class FiscalNote(BaseFiscalNote, table=True):
    __tablename__ = "fiscal_notes"

    id: UUID = Field(
        default_factory=uuid4,
        description="Fiscal note ID",
        sa_column=Column("id", GUID(), primary_key=True),
    )
    owner_id: UUID = Field(
        default_factory=uuid4, description="User ID that owns the fiscal note", foreign_key="users.id"
    )
    file_id: str = Field(..., description="Identation of file in storage service", foreign_key="files.bucket_key")

    file: File = Relationship()
    owner: User = Relationship()
    items: List[FiscalNoteItem] = Relationship(
        sa_relationship_kwargs={"cascade": "all,delete", "lazy": "selectin", "passive_deletes": True}
    )
