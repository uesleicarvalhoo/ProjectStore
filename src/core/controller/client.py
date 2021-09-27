from typing import List

import inject
from sqlmodel import Session, select

from src.core.events import EventCode
from src.core.exceptions import DatabaseError, NotFoundError
from src.core.models import Client, Context, CreateClient, GetClient, UpdateClient
from src.core.services import Streamer


@inject.params(streamer=Streamer)
def create(session: Session, schema: CreateClient, context: Context, streamer: Streamer) -> Client:

    if session.exec(select(Client).where(Client.email == schema.email)).scalar():
        raise DatabaseError("Já existe um cliente cadastrado com o email: %s" % schema.email)

    if session.exec(select(Client).where(Client.phone == schema.phone)).scalar():
        raise DatabaseError("Já existe um cliente cadastrado com o telefone: %s" % schema.phone)

    client = Client(**schema.dict())
    session.add(client)
    session.commit()
    streamer.send_event(EventCode.CREATE_USER, context=context, client=client.dict())

    return client


def get_all(session: Session, query: GetClient, context: Context) -> List[Client]:
    return session.exec(select(Client)).scalars()


def get_by_id(session: Session, client_id: int, context: Context) -> Client:
    client = session.exec(select(Client).where(Client.id == client_id))

    if not client:
        raise NotFoundError(f"Não foi possível localizar o Client com ID: {client_id}")

    return client


@inject.params(streamer=Streamer)
def delete(session: Session, client_id: int, context: Context, streamer: Streamer) -> Client:
    client = session.exec(select(Client).where(Client.id == client_id)).scalar()

    if not client:
        raise NotFoundError(f"Não foi possível localizar o Client com ID: {client_id}")

    session.delete(client)
    session.commit()

    streamer.send_event(event_code=EventCode.DELETE_ITEM, context=context, client=client.dict())

    return client


@inject.params(streamer=Streamer)
def update(session: Session, data: UpdateClient, context: Context, streamer: Streamer) -> Client:
    client = session.exec(select(Client).where(Client.id == data.id)).scalar()

    if not client:
        raise NotFoundError(f"Não foi possível localizar o Client com ID: {data.id}")

    columns = client.__table__.columns.keys()

    for key, value in data.items():
        if key not in columns:
            continue

        setattr(client, key, value)

    streamer.send_event(
        event_code=EventCode.UPDATE_CLIENT,
        context=context,
        data={"client_data": client.dict(), "update_schema": data.dict()},
    )
