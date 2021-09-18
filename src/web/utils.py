import inject
from fastapi import Request
from fastapi.templating import Jinja2Templates

from src.core.config import AppSettings, settings
from src.core.constants import OrderEnum
from src.core.schemas import Message
from src.core.services import CacheClient

templates = Jinja2Templates(directory="src/web/templates")
templates.env.globals.update(
    {
        "settings": AppSettings(),
        "round": round,
        "OrderEnum": OrderEnum,
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
