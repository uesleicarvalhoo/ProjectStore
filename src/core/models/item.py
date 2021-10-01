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
    code: str = Field(..., description="Código do produto")
    name: str = Field(..., description="Nome do item")
    avaliable: bool = Field(..., description="Item disponível")
    buy_value: PositiveFloat = Field(..., description="Valor de compra do item")
    sugested_sell_value: PositiveFloat = Field(..., description="Valor de venda sugerido")


class CreateItem(BaseItem):
    image: bytes = Field(..., description="String contendo o Base64 da imagem")
    filename: str = Field(..., description="Nome do arquivo da imagem")

    @validator("image", pre=True)
    def validate_image(cls, value: str) -> bytes:
        try:
            return b64decode(value)

        except Exception:
            apm.capture_exception()
            raise ValueError("Não foi possível decodificar o arquivo!")

    @property
    def file_extension(self) -> str:
        return self.filename.split(".")[-1]


class GetItem(BaseQuerySchema):
    id: UUID = Field(None, description="ID do item")
    avaliable: bool = Field(None, description="Items disponíveis/indisponíveis (None será ignorado)")


class Item(BaseItem, table=True):
    __tablename__ = "items"

    id: UUID = Field(
        default_factory=uuid4,
        description="ID do item",
        sa_column=Column("id", GUID(), default=uuid4(), primary_key=True),
    )
    fiscal_note_id: UUID = Field(..., description="ID da nota fiscal", foreign_key="fiscal_notes.id")
    file_id: UUID = Field(..., description="ID do arquivo no banco de dados", foreign_key="files.bucket_key")

    file: "File" = Relationship()
    fiscal_note: "FiscalNote" = Relationship(
        back_populates="items",
        sa_relationship_kwargs={"cascade": "all,delete", "lazy": "selectin", "passive_deletes": True},
    )
