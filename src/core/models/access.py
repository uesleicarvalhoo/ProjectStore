from uuid import UUID

from pydantic import BaseModel
from pydantic.fields import Field


class Token(BaseModel):
    sub: UUID = Field(..., description="Acess token")
    exp: int = Field(..., description="Type of authentication")
    created_at: int = Field(..., description="Timestamp of create time")
