from typing import Optional, Union
from uuid import UUID

from pydantic import BaseModel

from src.core.constants import ContextEnum


class Message(BaseModel):
    header: str
    text: str


class Context(BaseModel):
    context: ContextEnum
    user_id: Union[UUID, int, str, None]
    method: str
    authenticated: bool = False
    message: Optional[Message]

    def send_message(self, header: str, text: str) -> None:
        self.message = Message(header=header, text=text)
