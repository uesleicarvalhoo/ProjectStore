from typing import Union
from uuid import UUID

from pydantic import BaseModel

from src.core.constants import AccessLevel, ContextEnum


class Context(BaseModel):
    context: ContextEnum
    user_id: Union[UUID, None]
    user_access_level: bool = False
    method: str
    authenticated: bool = False

    @property
    def user_is_super_user(self) -> bool:
        return self.user_access_level == AccessLevel.SUPER_USER
