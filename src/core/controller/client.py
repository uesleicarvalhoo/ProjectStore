from typing import List
from uuid import UUID

import inject
from sqlmodel import Session, select

from src.core.events import EventCode
from src.core.helpers.exceptions import DatabaseError, NotAuthorizedError, NotFoundError
from src.core.models import Client, Context, CreateClient, QueryClient, UpdateClient
from src.core.services import Streamer


@inject.params(streamer=Streamer)
def create(session: Session, schema: CreateClient, context: Context, streamer: Streamer) -> Client:
    if session.exec(select(Client).where(Client.email == schema.email)).first():
        raise DatabaseError("Já existe um cliente cadastrado com o email: %s" % schema.email)

    if session.exec(select(Client).where(Client.phone == schema.phone)).first():
        raise DatabaseError("Já existe um cliente cadastrado com o telefone: %s" % schema.phone)

    client = Client(**schema.dict(), owner_id=context.user_id)
    session.add(client)
    session.commit()
    streamer.send_event(EventCode.CREATE_USER, context=context, client=client.dict())

    return client


def get_all(session: Session, query_schema: QueryClient, context: Context) -> List[Client]:
    query = select(Client).offset(query_schema.offset)

    if not context.current_user_is_super_user:
        query = query.where(Client.owner_id == context.user_id)

    if query_schema.limit > 0:
        query = query.limit(query_schema.limit)

    return session.exec(query).all()


def get_by_id(session: Session, client_id: UUID, context: Context) -> Client:
    client = session.exec(select(Client).where(Client.id == client_id)).first()

    if not client:
        raise NotFoundError(f"Não foi possível localizar o Client com ID: {client_id}")

    if not context.current_user_is_super_user and client.owner_id != context.user_id:
        raise NotAuthorizedError(f"Você não possui perimssão para consultar os dados do cliente com ID {client_id}!")

    return client


@inject.params(streamer=Streamer)
def delete(session: Session, client_id: UUID, context: Context, streamer: Streamer) -> Client:
    client = session.exec(select(Client).where(Client.id == client_id)).first()

    if not client:
        raise NotFoundError(f"Não foi possível localizar o Cliente com ID: {client_id}")

    if not context.current_user_is_super_user and client.owner_id != context.user_id:
        raise NotAuthorizedError(f"Você não possui permissão para excluir o Cliente com ID: {client_id}")

    session.delete(client)
    session.commit()

    streamer.send_event(event_code=EventCode.DELETE_ITEM, context=context, client=client.dict())

    return client


@inject.params(streamer=Streamer)
def update(session: Session, data: UpdateClient, context: Context, streamer: Streamer) -> None:
    client = session.exec(select(Client).where(Client.id == data.id)).first()

    if not client:
        raise NotFoundError(f"Não foi possível localizar o Client com ID: {data.id}")

    if not context.current_user_is_super_user and client.owner_id != context.user_id:
        raise NotAuthorizedError(f"Você não possui permissão para excluir o Cliente com ID: {data.id}")

    columns = client.__table__.columns.keys()

    for key, value in data:
        if key not in columns:
            continue

        setattr(client, key, value)

    session.add(client)
    session.commit()

    streamer.send_event(
        event_code=EventCode.UPDATE_CLIENT,
        context=context,
        data={"client_data": client.dict(), "update_schema": data.dict()},
    )
