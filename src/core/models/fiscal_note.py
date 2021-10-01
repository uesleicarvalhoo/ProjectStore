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
    description: str = Field(..., description="Descrição da nota fiscal")
    purchase_date: date = Field(..., description="Data da compra")


class CreateFiscalNote(BaseFiscalNote):
    image: bytes = Field(..., description="String contendo o Base64 da imagem")
    filename: str = Field(..., description="Nome do arquivo da imagem")
    items: List[CreateItem] = Field([], description="Lista de items da nota fiscal")

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


class GetFiscalNote(BaseQuerySchema):
    id: int = Field(None, description="ID da nota fiscal")


class FiscalNote(BaseFiscalNote, table=True):
    __tablename__ = "fiscal_notes"

    id: UUID = Field(
        default_factory=uuid4,
        description="ID da nota fiscal",
        sa_column=Column("id", GUID(), default=uuid4(), primary_key=True),
    )
    file_id: UUID = Field(..., description="ID do arquivo da nota fiscal", foreign_key="files.bucket_key")

    file: File = Relationship()
    items: List[Item] = Relationship(
        sa_relationship_kwargs={"cascade": "all,delete", "lazy": "selectin", "passive_deletes": True}
    )
