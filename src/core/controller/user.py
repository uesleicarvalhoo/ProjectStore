from typing import List
from uuid import UUID

import inject
from pydantic import EmailStr
from sqlmodel import Session, select

from src.core.events import EventDescription
from src.core.helpers.exceptions import DatabaseError, InvalidCredentialError, NotAuthorizedError, NotFoundError
from src.core.models import Context, CreateUser, QueryUser, UpdateUser, User
from src.core.models.user import UpdateUserPassword
from src.core.security import get_password_hash, verify_password
from src.core.services import Streamer


@inject.params(streamer=Streamer)
def create(session: Session, schema: CreateUser, context: Context, streamer: Streamer) -> User:
    if session.exec(select(User).where(User.email == schema.email)).first():
        raise DatabaseError("Já existe um usuário cadastrado com o email: %s" % schema.email)

    data = schema.dict(exclude={"confirm_password": ...})
    data["password_hash"] = get_password_hash(data.pop("password"))

    user = User(**data)
    session.add(user)
    session.commit()

    streamer.send_event(description=EventDescription.CREATE_USER, context=context, **{"user": user.dict()})

    return user


def get_by_id(session: Session, user_id: UUID, context: Context) -> User:
    user = session.exec(select(User).where(User.id == user_id)).first()

    if not user:
        raise NotFoundError("Não foi possível localizar o usuário com o ID: %s" % user_id)

    return user


def get_by_email(session: Session, email: EmailStr, context: Context) -> User:
    user = session.exec(select(User).where(User.email == email)).first()

    if not user:
        raise NotFoundError("Não foi possível localizar o usuário com o Email: %s" % email)

    return user


@inject.params(streamer=Streamer)
def update_by_id(session: Session, user_id: UUID, data: UpdateUser, context: Context, streamer: Streamer) -> User:
    user = session.exec(select(User).where(User.id == user_id)).first()

    if not user:
        raise NotFoundError(f"Não foi possível localizar o usuário com ID: {user_id}")

    if not context.user_is_super_user and user_id != context.user_id:
        raise NotAuthorizedError(f"Você não possui permissão para excluir a venda com ID: {user_id}")

    columns = user.__table__.columns.keys()

    for key, value in data.dict(exclude_defaults=True, exclude={"password_hash": ...}).items():
        if key not in columns:
            continue

        setattr(user, key, value)

    session.add(user)
    session.commit()

    streamer.send_event(
        description=EventDescription.UPDATE_USER,
        context=context,
        data={"order_data": user.dict(), "update_schema": data.dict()},
    )

    return user


def update_password(session: Session, user_id: UUID, schema: UpdateUserPassword, context: Context) -> None:
    user = session.exec(select(User).where(User.id == user_id)).first()

    if not user:
        raise NotFoundError("Não foi possível localizar o usuário com o ID: %s" % user_id)

    if not verify_password(schema.current_password, user.password_hash):
        raise InvalidCredentialError("Senha invalida")

    user.password_hash = get_password_hash(schema.new_password)
    session.add(user)
    session.commit()


def get_all(session: Session, query_schema: QueryUser, context: Context) -> List[User]:
    return session.exec(select(User)).all()


@inject.params(streamer=Streamer)
def delete(session: Session, user_id: UUID, context: Context, streamer: Streamer) -> User:
    user = session.exec(select(User).where(User.id == user_id)).first()

    if not user:
        raise NotFoundError(f"Não foi possível localiazar o usuário com ID: {user_id}")

    session.delete(user)
    streamer.send_event(EventDescription.DELETE_USER, context=context, user=user.dict())

    return user


def authenticate(session: Session, email: EmailStr, password: str, context: Context) -> User:
    user = session.exec(select(User).where(User.email == email)).first()

    if not user:
        raise InvalidCredentialError(f'Usuário "{email}" não localizado!')

    if not verify_password(password, user.password_hash):
        raise InvalidCredentialError("Senha invalida")

    return user
