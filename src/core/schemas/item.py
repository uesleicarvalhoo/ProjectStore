from base64 import b64decode

from pydantic import BaseModel, validator
from pydantic.fields import Field
from pydantic.types import PositiveFloat

from src.apm import apm

from .base import BaseQuerySchema
from .file import File


class BaseItem(BaseModel):
    code: str = Field(..., description="Código do produto")
    name: str = Field(..., description="Nome do item")
    avaliable: bool = Field(..., description="Item disponível")
    buy_value: PositiveFloat = Field(..., description="Valor de compra do item")
    sugested_sell_value: PositiveFloat = Field(..., description="Valor de venda sugerido")


class Item(BaseItem):
    id: int = Field(..., description="ID do item")
    fiscal_note_id: int = Field(..., description="ID da nota fiscal")
    file_id: str = Field(..., description="ID do arquivo no banco de dados")
    file: File = Field(..., description="Informações do arquivo que contém o Item")

    class Config:
        orm_mode: bool = True


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


class GetItem(BaseQuerySchema):
    id: int = Field(None, description="ID do item")
    avaliable: bool = Field(None, description="Items disponíveis/indisponíveis (None será ignorado)")
