from base64 import b64decode
from datetime import date
from typing import List

from pydantic import BaseModel, Field, validator

from src.apm import apm

from .base import BaseQuerySchema
from .file import File
from .item import CreateItem, Item


class BaseFiscalNote(BaseModel):
    description: str = Field(..., description="Descrição da nota fiscal")
    purchase_date: date = Field(..., description="Data da compra")


class FiscalNote(BaseFiscalNote):
    id: int = Field(..., description="ID da nota fiscal")
    file: File = Field(..., description="Informações do arquivo que contém a nota fiscal")

    items: List[Item] = Field([], description="Lista de itens da nota fiscal")

    class Config:
        orm_mode: bool = True


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


class GetFiscalNote(BaseQuerySchema):
    id: int = Field(None, description="ID da nota fiscal")
