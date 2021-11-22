from datetime import timedelta
from time import time
from typing import Tuple, Union

from jose import jwt
from jose.exceptions import ExpiredSignatureError
from passlib.context import CryptContext
from pydantic.error_wrappers import ValidationError

from src.core.constants import AccessLevel
from src.core.helpers.exceptions import NotAuthorizedError
from src.monitoring import capture_exception
from src.utils.date import now_datetime

from .config import settings
from .models import ParsedToken

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


ALGORITHM = "HS256"


def create_access_token(
    subject: str, access_level: AccessLevel, expires_delta: Union[int, timedelta] = None
) -> Tuple[str, int]:
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

    return token, expire


def load_jwt_token(token: str) -> ParsedToken:
    if not token:
        raise NotAuthorizedError("Token invalido")

    try:
        return ParsedToken(**jwt.decode(token, settings.SECRET_KEY, algorithms=[ALGORITHM]))

    except ExpiredSignatureError:
        capture_exception()
        raise NotAuthorizedError("Sessão expirada")

    except (jwt.JWTError, ValidationError):
        capture_exception()
        raise NotAuthorizedError("Não foi possível validar as suas credenciais")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def generate_password_reset_token(email: str) -> str:
    delta = timedelta(hours=settings.RESET_TOKEN_EXPIRE_HOURS)
    now = now_datetime()
    expires = now + delta
    exp = expires.timestamp()
    encoded_jwt = jwt.encode(
        {"exp": exp, "nbf": now, "sub": email},
        settings.SECRET_KEY,
        algorithm=ALGORITHM,
    )
    return encoded_jwt


def verify_password_reset_token(token: str) -> Union[str, None]:
    try:
        decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=[ALGORITHM])
        return decoded_token["sub"]
    except jwt.JWTError:
        return None
