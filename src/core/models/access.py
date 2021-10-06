from uuid import UUID

from pydantic import BaseModel
from pydantic.fields import Field

from src.core.constants import AccessLevel


class Token(BaseModel):
    sub: UUID = Field(..., description="Acess token")
    exp: int = Field(..., description="Timestamp that expire authentication")
    access_level: AccessLevel = Field(..., description="Group of User")
    created_at: int = Field(..., description="Timestamp of create time")
