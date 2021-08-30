from typing import List

import inject
from sqlalchemy.orm import Session

from src.core.database.models import User as UserModel
from src.core.events import EventCode
from src.core.exceptions import DatabaseError, InvalidCredentialError, NotFoundError
from src.core.schemas import Context, CreateUser, GetUser
from src.core.security import verify_password
from src.core.services import Streamer


@inject.params(streamer=Streamer)
def create(session: Session, schema: CreateUser, context: Context, streamer: Streamer) -> UserModel:
    if UserModel.exists(session, schema.email):
        raise DatabaseError("Já existe um usuário cadastrado com o email: %s" % schema.email)

    user = UserModel.create(session, schema)
    streamer.send_event(event_code=EventCode.CREATE_USER, context=context, **{"user": user.dict()})

    return user


def get_by_id(session: Session, user_id: int, context: Context) -> UserModel:
    user = UserModel.get(session, user_id)

    if not user:
        raise NotFoundError("Não foi possível localizar o usuário com o ID: %s" % user_id)

    return user


def get_all(session: Session, query: GetUser, context: Context) -> List[UserModel]:
    return UserModel.get_all(session, query)


@inject.params(streamer=Streamer)
def delete(session: Session, user_id: int, context: Context, streamer: Streamer) -> UserModel:
    user = UserModel.delete_by_id(session, user_id)

    if not user:
        raise NotFoundError(f"Não foi possível localiazar o usuário com ID: {user_id}")

    streamer.send_event(EventCode.DELETE_USER, context=context, user=user.dict())

    return user


def authenticate(session: Session, email: str, password: str, context: Context) -> UserModel:
    user = UserModel.get_by_email(session, email)

    if not user:
        raise InvalidCredentialError('Usuário "{username}" não localizado!')

    if not verify_password(password, user.password_hash):
        raise InvalidCredentialError("Senha invalida")

    return user
