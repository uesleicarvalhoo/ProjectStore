from datetime import timedelta
from time import time
from typing import Union

import inject
from jose import jwt
from jose.exceptions import ExpiredSignatureError
from passlib.context import CryptContext
from pydantic.error_wrappers import ValidationError
from starlette.responses import Response

from src.apm import apm
from src.core.constants import AccessLevel
from src.core.helpers.exceptions import NotAuthorizedError
from src.core.services import CacheClient
from src.utils.date import now_datetime

from .config import settings
from .models import Token

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


ALGORITHM = "HS256"


def create_access_token(subject: str, access_level: AccessLevel, expires_delta: Union[int, timedelta] = None) -> str:
    if not subject:
        raise ValueError("Subject can't be null!")

    if expires_delta is None:
        expires_delta = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    if isinstance(expires_delta, int):
        expires_delta = timedelta(minutes=expires_delta)

    now = now_datetime()
    expire = now + expires_delta

    to_encode = {"exp": expire, "sub": subject, "created_at": time(), "access_level": access_level}

    token = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)

    return token


def load_jwt_token(token: str) -> Token:
    try:
        return Token(**jwt.decode(token, settings.SECRET_KEY, algorithms=[ALGORITHM]))

    except ExpiredSignatureError:
        apm.capture_exception()
        raise NotAuthorizedError("Sessão expirada")

    except (jwt.JWTError, ValidationError):
        apm.capture_exception()
        raise NotAuthorizedError("Não foi possível validar as suas credenciais")


@inject.params(cache=CacheClient)
def validate_access_token(token: str, cache: CacheClient) -> bool:
    try:
        load_jwt_token(token=token)
    except NotAuthorizedError:
        return False

    return cache.get("token-black-list", token) is None


@inject.params(cache=CacheClient)
async def invalidate_access_token(jwt_token: str, cache: CacheClient, response: Response = None) -> None:
    token = load_jwt_token(jwt_token)
    expire = int(token.exp - now_datetime().timestamp())
    cache.set("token-black-list", jwt_token, token, expire)

    if response:
        response.delete_cookie(settings.ACCESS_TOKEN_NAME)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)
