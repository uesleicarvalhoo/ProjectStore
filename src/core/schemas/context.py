from typing import List, Union
from uuid import UUID

from pydantic import BaseModel

from src.core.constants import ContextEnum


class Message(BaseModel):
    header: str
    text: str


class Context(BaseModel):
    context: ContextEnum
    user_id: Union[UUID, int, str]
    method: str
    authenticated: bool = False
    messages: List[Message] = []

    def add_message(self, header: str, text: str) -> None:
        self.messages.append(Message(header=header, text=text))
