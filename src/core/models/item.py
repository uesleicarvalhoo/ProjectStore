from base64 import b64decode
from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from pydantic import PositiveFloat, validator
from sqlmodel import Column, Field, Relationship, SQLModel

from src.apm import apm

from .base import BaseQuerySchema
from .types import GUID

if TYPE_CHECKING:
    from .file import File
    from .fiscal_note import FiscalNote


class BaseItem(SQLModel):
    code: str = Field(..., description="Item code")
    name: str = Field(..., description="Item Name")
    avaliable: bool = Field(..., description="Flag to identify if the item is avaliable")
    buy_value: PositiveFloat = Field(..., description="Buy value of item")
    sugested_sell_value: PositiveFloat = Field(..., description="Sugested sell value of item")


class CreateItem(BaseItem):
    image: bytes = Field(..., description="Content base64 of the image")
    filename: str = Field(..., description="Image filename")

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


class GetItem(BaseQuerySchema):
    id: UUID = Field(None, description="Item ID")
    avaliable: bool = Field(None, description="Flag to identify if the item is avaliable")


class Item(BaseItem, table=True):
    __tablename__ = "items"

    id: UUID = Field(default_factory=uuid4, description="ID do item", sa_column=Column("id", GUID(), primary_key=True))
    fiscal_note_id: UUID = Field(..., description="Fiscal Note ID", foreign_key="fiscal_notes.id")
    file_id: str = Field(..., description="Identation of file in storage service", foreign_key="files.bucket_key")

    file: "File" = Relationship()
    fiscal_note: "FiscalNote" = Relationship(
        back_populates="items",
        sa_relationship_kwargs={"cascade": "all,delete", "lazy": "selectin", "passive_deletes": True},
    )
