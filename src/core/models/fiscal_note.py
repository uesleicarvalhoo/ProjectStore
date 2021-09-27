from base64 import b64decode
from datetime import date
from typing import List

from pydantic import validator
from sqlmodel import Field, Relationship, SQLModel

from src.apm import apm

from .base import BaseQuerySchema, common_relationship_kwargs
from .file import File
from .item import CreateItem, Item


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

    id: int = Field(..., description="ID da nota fiscal", primary_key=True)
    file_id: str = Field(..., description="ID do arquivo da nota fiscal", foreign_key="files.bucket_key")

    file: File = Relationship(sa_relationship_kwargs=common_relationship_kwargs)
    items: List[Item] = Relationship(sa_relationship_kwargs=common_relationship_kwargs)
