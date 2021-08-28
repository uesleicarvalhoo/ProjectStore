from typing import Union

from fastapi import Request
from fastapi.param_functions import Depends
from fastapi.params import Cookie
from sqlalchemy.orm import Session

from src.core.config import AppSettings, settings
from src.core.constants import ContextEnum
from src.core.database import make_session
from src.core.database.models import User
from src.core.exceptions import NotAuthorizedError
from src.core.schemas import Context, Token
from src.core.security import load_jwt_token, validate_access_token


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

        # TODO: Carregar as mensagens no contexto, utilizar o redis(?)
        return Context(context=self.context, user_id=user_id, method=request.url.path, authenticated=authenticated)


def make_settings() -> AppSettings:
    return AppSettings()


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
    user = User.get(session, token.sub)

    if not user:
        raise NotAuthorizedError("Usuário não localizado")

    return user


async def validate_user_admin(user: User = Depends(get_current_user)) -> None:
    if not user.admin:
        raise NotAuthorizedError("Essa página só está disponível para administradores")


context_manager = ContextManager(ContextEnum.WEB)
