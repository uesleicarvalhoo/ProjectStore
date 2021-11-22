from datetime import datetime

from pydantic import BaseModel
from sqlmodel import Field, SQLModel

from ...utils.date import now_datetime
from ..config import settings


class CreateFile(SQLModel):
    data: bytes = Field(description="Content of File")
    filename: str = Field(description="Name of file", min_length=1)


class QueryFile(SQLModel):
    bucket_key: str = Field(description="Identation of file in storage service")


class DeleteFile(BaseModel):
    bucket_key: str = Field(description="Identation of file in storage service")


class File(SQLModel, table=True):
    __tablename__ = "files"

    bucket_key: str = Field(description="Identation of file in storage service", primary_key=True)
    hash: str = Field(description="Hash of file")

    uploaded_at: datetime = Field(default_factory=now_datetime, description="Datetime of the file update")

    @property
    def src_url(self) -> str:
        return f"{settings.STORAGE_URL.rstrip('/')}/{settings.STORAGE_BUCKET}/{self.bucket_key}".replace("%", "%25")
