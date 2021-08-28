from datetime import timedelta
from time import time
from typing import Union

from jose import jwt
from jose.exceptions import ExpiredSignatureError
from passlib.context import CryptContext
from pydantic.error_wrappers import ValidationError
from starlette.responses import Response

from src.apm import apm
from src.core.exceptions import NotAuthorizedError
from src.utils.date import now_datetime
from src.utils.miscellaneous import cache

from .config import settings
from .schemas import Token

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


ALGORITHM = "HS256"


def create_access_token(subject: str, expires_delta: Union[int, timedelta] = None) -> str:
    if expires_delta is None:
        expires_delta = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    if isinstance(expires_delta, int):
        expires_delta = timedelta(minutes=expires_delta)

    now = now_datetime()
    expire = now + expires_delta

    to_encode = {"exp": expire, "sub": subject, "created_at": time()}

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


def validate_access_token(token: str) -> bool:
    try:
        load_jwt_token(token=token)
    except NotAuthorizedError:
        return False

    return cache.get("token-black-list", token) is None


async def invalidate_access_token(jwt_token: str, response: Response = None) -> None:
    token = load_jwt_token(jwt_token)
    expire = int(token.exp - now_datetime().timestamp())
    cache.set("token-black-list", jwt_token, token, expire)

    if response:
        response.delete_cookie(settings.ACCESS_TOKEN_NAME)


async def refresh_access_token(response: Response, token: str, expires_delta: Union[int, timedelta] = None) -> None:
    parsed_token = load_jwt_token(token)

    if not validate_access_token(token):
        return None

    if parsed_token.created_at + (settings.ACESS_TOKEN_REFRESH_MINUTES * 60) > time():
        return None

    await invalidate_access_token(jwt_token=token, response=response)
    await set_token_on_response(response, token=create_access_token(str(parsed_token.sub), expires_delta))


async def set_token_on_response(response: Response, token: str) -> None:
    parsed_token = load_jwt_token(token)
    response.set_cookie(settings.ACCESS_TOKEN_NAME, token, max_age=parsed_token.exp)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)
