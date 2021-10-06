from datetime import timedelta
from time import time
from typing import Union

import inject
from fastapi import Request, Response
from fastapi.param_functions import Cookie, Depends, Header
from sqlmodel import Session, select

from ..core.config import settings
from ..core.constants import AccessLevel, ContextEnum
from ..core.helpers.database import make_session
from ..core.helpers.exceptions import NotAuthorizedError
from ..core.models import Context, Message, Token, User
from ..core.security import create_access_token, invalidate_access_token, load_jwt_token, validate_access_token
from ..core.services import CacheClient


class ContextManager:
    context: ContextEnum

    def __init__(self, context: Union[str, ContextEnum]) -> None:
        self.context = context if isinstance(context, ContextEnum) else ContextEnum(context)

    def __call__(self, request: Request) -> Context:
        token = request.cookies.get(settings.ACCESS_TOKEN_NAME)

        try:
            parsed_token = get_parsed_token(token=token)
            user_id = parsed_token.sub
            access_level = parsed_token.access_level
            authenticated = validate_access_token(token)

        except NotAuthorizedError:
            user_id = "anonymous"
            authenticated = False
            access_level = AccessLevel.ANONIMOUS

        return Context(
            context=self.context,
            user_id=user_id,
            method=request.url.path,
            authenticated=authenticated,
            access_level=access_level,
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


def get_token(
    cookie_token: str = Cookie(None, alias="access_token"), header_token: str = Header(None, alias="access_token")
) -> str:
    access_token = header_token or cookie_token

    if not access_token:
        raise NotAuthorizedError("Você precisa fazer login antes de continuar")

    return access_token


def get_parsed_token(token: str = Depends(get_token)) -> Token:
    if not token:
        raise NotAuthorizedError("Você precisa fazer login antes de continuar")

    return load_jwt_token(token)


async def get_current_user(session: Session = Depends(make_session), token: Token = Depends(get_parsed_token)) -> User:
    user = session.exec(select(User).where(User.id == token.sub)).first()

    if not user:
        raise NotAuthorizedError("Usuário não localizado")

    return user


async def login_required(token: Token = Depends(get_token), current_user: User = Depends(get_current_user)) -> None:
    if not validate_access_token(token):
        raise NotAuthorizedError("Sessão expirada!")

    if not current_user.is_active:
        raise NotAuthorizedError("Sua licença expirou! Entre em contato com um administrador.")


async def validate_super_user(user: User = Depends(get_current_user)) -> None:
    if not user.admin:
        raise NotAuthorizedError("Essa página só está disponível para administradores")


async def refresh_access_token(response: Response, token: str, expires_delta: Union[int, timedelta] = None) -> None:
    parsed_token = load_jwt_token(token)

    if not validate_access_token(token):
        return None

    if parsed_token.created_at + (settings.ACESS_TOKEN_REFRESH_MINUTES * 60) > time():
        return None

    await invalidate_access_token(jwt_token=token, response=response)
    await set_token_on_response(
        response,
        token=create_access_token(
            str(parsed_token.sub), access_level=parsed_token.access_level, expires_delta=expires_delta
        ),
    )


async def set_token_on_response(response: Response, token: str) -> None:
    parsed_token = load_jwt_token(token)
    response.set_cookie(settings.ACCESS_TOKEN_NAME, token, max_age=parsed_token.exp)


web_context_manager = ContextManager(ContextEnum.WEB)
api_context_manager = ContextManager(ContextEnum.API)
