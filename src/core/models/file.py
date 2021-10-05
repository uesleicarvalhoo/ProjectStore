from datetime import datetime

from pydantic import BaseModel
from sqlmodel import Field, SQLModel

from ...utils.date import now_datetime
from ..config import settings
from .base import BaseQuerySchema


class BaseFile(SQLModel):
    bucket_key: str = Field(..., description="Identation of file in storage service", primary_key=True)
    hash: str = Field(..., description="Hash of file")


class CreateFile(BaseFile):
    pass


class QueryFile(BaseQuerySchema):
    bucket_key: str = Field(..., description="Identation of file in storage service")


class DeleteFile(BaseModel):
    bucket_key: str = Field(..., description="Identation of file in storage service")


class File(BaseFile, table=True):
    __tablename__ = "files"

    uploaded_at: datetime = Field(default_factory=now_datetime, description="Datetime of the file update")

    @property
    def src_url(self) -> str:
        return f"{settings.STATIC_FILES_HOST}/{self.bucket_key}"
