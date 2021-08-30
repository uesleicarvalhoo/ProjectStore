from typing import List

import inject
from sqlalchemy.orm import Session

from src.core.database.models import Client as ClientModel
from src.core.events import EventCode
from src.core.exceptions import DatabaseError, NotFoundError
from src.core.schemas import Context, CreateClient, GetClient, UpdateClient
from src.core.services import Streamer


@inject.params(streamer=Streamer)
def create(session: Session, schema: CreateClient, context: Context, streamer: Streamer) -> ClientModel:
    if ClientModel.exists(session, email=schema.email):
        raise DatabaseError("Já existe um cliente cadastrado com o email: %s" % schema.email)

    if ClientModel.exists(session, phone=schema.phone):
        raise DatabaseError("Já existe um cliente cadastrado com o telefone: %s" % schema.phone)

    client = ClientModel.create(session, schema)
    streamer.send_event(EventCode.CREATE_USER, context=context, **{"client": client})

    return client


def get_all(session: Session, query: GetClient, context: Context) -> List[ClientModel]:
    return ClientModel.get_all(session, query)


def get_by_id(session: Session, client_id: int, context: Context) -> ClientModel:
    client = ClientModel.get(session, client_id)

    if not client:
        raise NotFoundError(f"Não foi possível localizar o Client com ID: {client_id}")

    return client


@inject.params(streamer=Streamer)
def delete(session: Session, client_id: int, context: Context, streamer: Streamer) -> ClientModel:
    client = ClientModel.delete_by_id(session, client_id)

    if not client:
        raise NotFoundError(f"Não foi possível localizar o Client com ID: {client_id}")

    streamer.send_event(event_code=EventCode.DELETE_ITEM, context=context, client=client.dict())

    return client


@inject.params(streamer=Streamer)
def update(session: Session, data: UpdateClient, context: Context, streamer: Streamer) -> ClientModel:
    client = ClientModel.get(session, data.id)

    if not client:
        raise NotFoundError(f"Não foi possível localizar o Client com ID: {data.id}")

    streamer.send_event(
        event_code=EventCode.UPDATE_CLIENT,
        context=context,
        data={"client_data": client.dict(), "update_schema": data.dict()},
    )

    return client.update(session, data, auto_commit=True)
