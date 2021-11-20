from uuid import UUID

from pydantic import BaseModel
from pydantic.fields import Field

from src.core.constants import AccessLevel


class Token(BaseModel):
    access_token: str = Field(..., description="Access token", alias="accessToken")
    grant_type: str = Field(..., description="Grant type", alias="grantType")


class ParsedToken(BaseModel):
    sub: UUID = Field(..., description="Acess token")
    exp: int = Field(..., description="Timestamp that expire authentication")
    access_level: AccessLevel = Field(..., description="Group of User")
    created_at: int = Field(..., description="Timestamp of create time")
