from typing import List

import inject
from sqlalchemy.future import select
from sqlmodel import Session

from src.core.events import EventCode
from src.core.exceptions import DatabaseError, InvalidCredentialError, NotFoundError
from src.core.models import Context, CreateUser, GetUser, User
from src.core.security import get_password_hash, verify_password
from src.core.services import Streamer


@inject.params(streamer=Streamer)
def create(session: Session, schema: CreateUser, context: Context, streamer: Streamer) -> User:
    if session.exec(select(User)).scalar():
        raise DatabaseError("Já existe um usuário cadastrado com o email: %s" % schema.email)

    data = schema.dict(exclude={"confirm_password"})
    data["password_hash"] = get_password_hash(data.pop("password"))

    user = User(**data)
    session.add(user)
    session.commit()

    streamer.send_event(event_code=EventCode.CREATE_USER, context=context, **{"user": user.dict()})

    return user


def get_by_id(session: Session, user_id: int, context: Context) -> User:
    user = session.exec(select(User).where(User.id == user_id)).scalar()

    if not user:
        raise NotFoundError("Não foi possível localizar o usuário com o ID: %s" % user_id)

    return user


def get_all(session: Session, query: GetUser, context: Context) -> List[User]:
    query_args = []  # TODO: Utilizar o operador "like"

    if query.email:
        query_args.append(User.email == query.email)

    return session.exec(select(User).where(*query_args)).scalars()


@inject.params(streamer=Streamer)
def delete(session: Session, user_id: int, context: Context, streamer: Streamer) -> User:
    user = session.exec(select(User).where(User.id == user_id))

    if not user:
        raise NotFoundError(f"Não foi possível localiazar o usuário com ID: {user_id}")

    session.delete(user)
    streamer.send_event(EventCode.DELETE_USER, context=context, user=user.dict())

    return user


def authenticate(session: Session, email: str, password: str, context: Context) -> User:
    user = session.exec(select(User).where(User.email == email)).scalar()

    if not user:
        raise InvalidCredentialError('Usuário "{username}" não localizado!')

    if not verify_password(password, user.password_hash):
        raise InvalidCredentialError("Senha invalida")

    return user
