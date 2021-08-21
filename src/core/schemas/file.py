from datetime import datetime

from pydantic import BaseModel
from pydantic.fields import Field

from .base import BaseQuerySchema


class BaseFile(BaseModel):
    bucket_key: str = Field(..., description="Key do Bucket que o arquivo ficará guardado no Storage")
    hash: str = Field(..., description="Hash do arquivo")


class File(BaseFile):
    uploaded_at: datetime = Field(..., description="Data e hora de atualização do arquivo")

    class Config:
        orm_mode: bool = True


class CreateFile(BaseFile):
    pass


class GetFile(BaseQuerySchema):
    bucket_key: str = Field(..., description="Key do Bucket que o arquivo ficará guardado no Storage")


class DeleteFile(BaseModel):
    bucket_key: str = Field(..., description="Key do Bucket que o arquivo ficará guardado no Storage")
