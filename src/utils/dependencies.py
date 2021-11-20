from typing import Union

import inject
from fastapi import Request
from fastapi.param_functions import Cookie, Depends, Header
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import Session, select

from ..core.config import settings
from ..core.constants import AccessLevel, ContextEnum
from ..core.helpers.database import make_session
from ..core.helpers.exceptions import NotAuthorizedError
from ..core.models import Context, Message, ParsedToken, User
from ..core.security import load_jwt_token, validate_access_token
from ..core.services import CacheClient

reusable_oauth2 = OAuth2PasswordBearer(tokenUrl="api/v1/auth/access-token")


def get_string_token(token: str = Header(None, alias="Authorization")) -> Union[None, str]:
    if token:
        _, token = token.split(" ", maxsplit=1)

    return token


def load_access_token(token: str = Depends(reusable_oauth2)) -> ParsedToken:
    return load_jwt_token(token)


def get_token(
    cookie_token: str = Cookie(None, alias="access_token"), header_token: str = Header(None, alias="access_token")
) -> str:
    access_token = header_token or cookie_token

    if not access_token:
        raise NotAuthorizedError("Você precisa fazer login antes de continuar")

    return access_token


def get_parsed_token(token: str = Depends(get_token)) -> ParsedToken:
    if not token:
        raise NotAuthorizedError("Você precisa fazer login antes de continuar")

    return load_jwt_token(token)


async def get_current_user(
    session: Session = Depends(make_session), token: ParsedToken = Depends(load_access_token)
) -> User:
    user = session.exec(select(User).where(User.id == token.sub)).first()

    if not user:
        raise NotAuthorizedError("Usuário não localizado")

    return user


async def login_required(
    token: ParsedToken = Depends(get_token), current_user: User = Depends(get_current_user)
) -> None:
    if not validate_access_token(token):
        raise NotAuthorizedError("Sessão expirada!")

    if not current_user.is_active:
        raise NotAuthorizedError("Sua licença expirou! Entre em contato com um administrador.")


async def validate_super_user(user: User = Depends(get_current_user)) -> None:
    if not user.is_super_user:
        raise NotAuthorizedError("Essa página só está disponível para administradores")


class ContextManager:
    context: ContextEnum

    def __init__(self, context: Union[str, ContextEnum]) -> None:
        self.context = context if isinstance(context, ContextEnum) else ContextEnum(context)

    def __call__(self, request: Request, token: str = Depends(get_string_token)) -> Context:
        try:
            parsed_token = get_parsed_token(token=token)
            user_id = parsed_token.sub
            access_level = parsed_token.access_level
            authenticated = True

        except NotAuthorizedError:
            user_id = None
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
        return request.cookies.get(settings.SESSION_KEY_NAME, "")

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


api_context_manager = ContextManager(ContextEnum.API)
