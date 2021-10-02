from base64 import b64decode
from datetime import date
from typing import List
from uuid import UUID, uuid4

from pydantic import validator
from sqlmodel import Column, Field, Relationship, SQLModel

from src.apm import apm

from .base import BaseQuerySchema
from .file import File
from .item import CreateItem, Item
from .types import GUID


class BaseFiscalNote(SQLModel):
    description: str = Field(..., description="Description of fiscal note")
    purchase_date: date = Field(..., description="Date of purchase")


class CreateFiscalNote(BaseFiscalNote):
    image: bytes = Field(..., description="Content base64 of the image")
    filename: str = Field(..., description="Image filename")
    items: List[CreateItem] = Field([], description="List of items in the fiscal note")

    @validator("image", pre=True)
    def validate_image(cls, value: str) -> bytes:
        try:
            return b64decode(value)

        except Exception:
            apm.capture_exception()
            raise ValueError("Couldn't decode the file!")

    @property
    def file_extension(self) -> str:
        return self.filename.split(".")[-1]


class GetFiscalNote(BaseQuerySchema):
    id: UUID = Field(None, description="Fiscal note ID")


class FiscalNote(BaseFiscalNote, table=True):
    __tablename__ = "fiscal_notes"

    id: UUID = Field(
        default_factory=uuid4,
        description="Fiscal note ID",
        sa_column=Column("id", GUID(), primary_key=True),
    )
    file_id: str = Field(..., description="Identation of file in storage service", foreign_key="files.bucket_key")

    file: File = Relationship()
    items: List[Item] = Relationship(
        sa_relationship_kwargs={"cascade": "all,delete", "lazy": "selectin", "passive_deletes": True}
    )