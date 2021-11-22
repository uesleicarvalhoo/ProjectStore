from datetime import datetime
from typing import Any, Dict
from uuid import UUID, uuid4

from pydantic import BaseModel, Field

from src.core.config import settings
from src.core.events import EventDescription

from .context import Context


class Event(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    application: str = Field(settings.APPLICATION_NAME)
    date_time: str = Field(default_factory=datetime.now)
    description: EventDescription
    data: Dict[str, Any]
    context: Context

    class Config:
        allow_population_by_field_name = True

        @classmethod
        def alias_generator(cls, string: str) -> str:
            words = string.split("_")
            return "".join(words[:1] + [word.capitalize() for word in words[1:]])
