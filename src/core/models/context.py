from typing import Optional, Union
from uuid import UUID

from pydantic import BaseModel

from src.core.constants import AccessLevel, ContextEnum


class Message(BaseModel):
    header: str
    text: str


class Context(BaseModel):
    context: ContextEnum
    user_id: Union[UUID, int, str, None]
    current_user_access_level: bool = False
    method: str
    authenticated: bool = False
    message: Optional[Message]

    def send_message(self, header: str, text: str) -> None:
        self.message = Message(header=header, text=text)

    @property
    def current_user_is_super_user(self) -> bool:
        return self.current_user_access_level == AccessLevel.SUPER_USER
