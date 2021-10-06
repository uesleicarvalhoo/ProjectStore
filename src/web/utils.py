import math

import inject
from fastapi import Request
from fastapi.templating import Jinja2Templates

from src.core.config import AppSettings, settings
from src.core.constants import AccessLevel, OrderStatus
from src.core.models import Message, User
from src.core.services import CacheClient

anonimous_user = User(
    name="Anonimous User",
    email="anonimous@email.com",
    access_level=AccessLevel.ANONIMOUS,
)

templates = Jinja2Templates(directory="src/web/templates")
templates.env.globals.update(
    {
        "math": math,
        "settings": AppSettings(),
        "round": round,
        "OrderStatus": OrderStatus,
        "current_user": anonimous_user,
    }
)


def _get_session_id(request: Request) -> str:
    return request.cookies.get(settings.SESSION_KEY_NAME)


@inject.params(cache=CacheClient)
def load_messages(request: Request, cache: CacheClient) -> Message:
    session_id = _get_session_id(request)
    message = cache.get("messages", session_id)

    if not message:
        return None

    cache.delete("messages", session_id)

    return Message(**message)


@inject.params(cache=CacheClient)
def send_message(request: Request, header: str, text: str, cache: CacheClient) -> None:
    session_id = _get_session_id(request)

    if not session_id:
        return None

    cache.set("messages", session_id, {"header": header, "text": text}, expiration=5 * 60)
