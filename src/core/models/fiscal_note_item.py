from base64 import b64decode
from typing import TYPE_CHECKING, Any, Dict, Optional, Union
from uuid import UUID, uuid4

from pydantic import validator
from sqlmodel import Column, Field, Relationship, SQLModel
from sqlmodel.sql.sqltypes import GUID

from src.monitoring import capture_exception

from .base import BaseQuerySchema
from .file import File
from .item import Item

if TYPE_CHECKING:
    from .fiscal_note import FiscalNote


class BaseFiscalNoteItem(SQLModel):
    buy_value: float = Field(..., description="Buy value of item")
    sugested_sell_value: float = Field(..., description="Sugested sell value of item")


class CreateFiscalNoteItem(BaseFiscalNoteItem):
    code: str = Field(..., description="Code of item", min_length=1)
    name: str = Field(..., description="Name of item", min_length=1)
    image: bytes = Field(..., description="Content base64 of the image")
    filename: str = Field(..., description="Image filename", min_length=1)

    @validator("image", pre=True)
    def validate_image(cls, value: Union[str, bytes]) -> bytes:
        if isinstance(value, bytes):
            return value

        try:
            return b64decode(value)

        except Exception:
            capture_exception()
            raise ValueError("Couldn't decode the file!")

    @validator("sugested_sell_value")
    def validate_sell_value(cls, value: Union[str, float], values: Dict[str, Any]) -> float:
        if isinstance(value, str):
            value = float(value)

        if values.get("buy_value", 0) >= value:
            raise ValueError("The sugested sell value must be higher then buy value!")

        return value

    @property
    def file_extension(self) -> str:
        return self.filename.split(".")[-1]


class QueryFiscalNoteItem(BaseQuerySchema):
    avaliable: Optional[bool] = Field(description="Flag to identify items avaliable")


class FiscalNoteItem(BaseFiscalNoteItem, table=True):
    __tablename__ = "fiscal_note_items"

    id: UUID = Field(
        default_factory=uuid4, description="ID of Fiscal Note Item", sa_column=Column("id", GUID(), primary_key=True)
    )
    owner_id: UUID = Field(description="User ID that owns the file", foreign_key="users.id")
    fiscal_note_id: UUID = Field(..., description="Fiscal Note ID", foreign_key="fiscal_notes.id")
    item_id: UUID = Field(..., description="Item ID", foreign_key="items.id")
    file_id: str = Field(..., description="Identation of file in storage service", foreign_key="files.bucket_key")

    fiscal_note: "FiscalNote" = Relationship(
        back_populates="items",
        sa_relationship_kwargs={"lazy": "selectin", "passive_deletes": True},
    )

    base_item: "Item" = Relationship(
        sa_relationship_kwargs={"lazy": "selectin", "passive_deletes": True},
    )

    file: "File" = Relationship()

    @property
    def sugested_sell_value(self) -> float:
        return self.item.value

    @property
    def name(self) -> str:
        return self.base_item.name

    @property
    def code(self) -> str:
        return self.base_item.code

    @property
    def amount(self) -> int:
        return self.base_item.amount
