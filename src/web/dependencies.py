from typing import Union

import inject
from fastapi import Request
from fastapi.param_functions import Depends
from fastapi.params import Cookie
from sqlmodel import Session, select

from src.core.config import settings
from src.core.constants import ContextEnum
from src.core.helpers.database import make_session
from src.core.helpers.exceptions import NotAuthorizedError
from src.core.models import Context, Message, Token, User
from src.core.security import load_jwt_token, validate_access_token
from src.core.services import CacheClient


class ContextManager:
    context: ContextEnum

    def __init__(self, context: Union[str, ContextEnum]) -> None:
        self.context = context if isinstance(context, ContextEnum) else ContextEnum(context)

    def __call__(self, request: Request) -> Context:
        token = request.cookies.get(settings.ACCESS_TOKEN_NAME)

        try:
            user_id = get_parsed_token(token=token).sub
            authenticated = validate_access_token(token)

        except NotAuthorizedError:
            user_id = "anonymous"
            authenticated = False

        return Context(
            context=self.context,
            user_id=user_id,
            method=request.url.path,
            authenticated=authenticated,
            message=self.load_message(request),
        )

    def _get_session_id(self, request: Request) -> str:
        return request.cookies.get(settings.SESSION_KEY_NAME)

    @inject.params(cache=CacheClient)
    def load_message(self, request: Request, cache: CacheClient) -> Message:
        session_id = self._get_session_id(request)
        message = cache.get("messages", session_id)

        if not message:
            return None

        cache.delete("messages", session_id)

        return Message(**message)

    @inject.params(cache=CacheClient)
    def send_message(self, request: Request, header: str, text: str, cache: CacheClient) -> None:
        session_id = self._get_session_id(request)

        if not session_id:
            return

        cache.set("messages", session_id, {"header": header, "text": text}, expiration=5 * 60)


def get_token(access_token: str = Cookie(None)) -> str:
    if not access_token:
        raise NotAuthorizedError("Você precisa fazer login antes de continuar")

    return access_token


def get_parsed_token(token: str = Depends(get_token)) -> Token:
    if not token:
        raise NotAuthorizedError("Você precisa fazer login antes de continuar")
    return load_jwt_token(token)


async def login_required(token: Token = Depends(get_token)) -> None:
    if not validate_access_token(token):
        raise NotAuthorizedError("Sessão expirada!")


async def get_current_user(session: Session = Depends(make_session), token: Token = Depends(get_parsed_token)) -> User:
    user = session.exec(select(User).where(User.id == token.sub)).first()

    if not user:
        raise NotAuthorizedError("Usuário não localizado")

    return user


async def validate_super_user(user: User = Depends(get_current_user)) -> None:
    if not user.admin:
        raise NotAuthorizedError("Essa página só está disponível para administradores")


context_manager = ContextManager(ContextEnum.WEB)
