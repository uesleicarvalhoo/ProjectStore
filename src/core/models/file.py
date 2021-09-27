from datetime import datetime

from pydantic import BaseModel
from sqlmodel import Field, SQLModel

from ...utils.date import now_datetime
from ..config import settings
from .base import BaseQuerySchema


class BaseFile(SQLModel):
    bucket_key: str = Field(..., description="Key do Bucket que o arquivo ficará guardado no Storage", primary_key=True)
    hash: str = Field(..., description="Hash do arquivo")


class CreateFile(BaseFile):
    pass


class GetFile(BaseQuerySchema):
    bucket_key: str = Field(..., description="Key do Bucket que o arquivo ficará guardado no Storage")


class DeleteFile(BaseModel):
    bucket_key: str = Field(..., description="Key do Bucket que o arquivo ficará guardado no Storage")


class File(BaseFile, table=True):
    __tablename__ = "files"

    uploaded_at: datetime = Field(default_factory=now_datetime, description="Data e hora de atualização do arquivo")

    @property
    def src_url(self) -> str:
        return f"{settings.STATIC_FILES_HOST}/{self.bucket_key}"
