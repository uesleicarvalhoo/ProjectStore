from typing import Union

from fastapi import Request
from fastapi.param_functions import Depends, Header
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import Session, select

from ..core.constants import AccessLevel, ContextEnum
from ..core.helpers.database import make_session
from ..core.helpers.exceptions import NotAuthorizedError
from ..core.models import Context, ParsedToken, User
from ..core.security import load_jwt_token

reusable_oauth2 = OAuth2PasswordBearer(tokenUrl="api/v1/auth/access-token")


def get_string_token(token: str = Header(None, alias="Authorization")) -> Union[None, str]:
    if token:
        _, _, token = token.partition(" ")

    return token


def load_access_token(token: str = Depends(reusable_oauth2)) -> ParsedToken:
    if not token:
        raise NotAuthorizedError("Token invalido")

    return load_jwt_token(token)


async def get_current_user(
    session: Session = Depends(make_session), token: ParsedToken = Depends(load_access_token)
) -> User:
    user = session.exec(select(User).where(User.id == token.sub)).first()

    if not user:
        raise NotAuthorizedError("Usuário não localizado")

    return user


async def login_required(current_user: User = Depends(get_current_user)) -> None:
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
            parsed_token = load_jwt_token(token=token)
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
        )


context_manager = ContextManager(ContextEnum.API)
