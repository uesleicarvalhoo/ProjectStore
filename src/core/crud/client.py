from typing import List

from sqlalchemy.orm import Session

from src.core.database.models import Client as ClientModel
from src.core.events import EventCode
from src.core.exceptions import DatabaseError, NotFoundError
from src.core.schemas import Context, CreateClient, GetClient
from src.core.services.streamer import Streamer


def create(session: Session, schema: CreateClient, context: Context, streamer: Streamer) -> ClientModel:
    if ClientModel.exists(session, email=schema.email):
        raise DatabaseError("Já existe um cliente cadastrado com o email: %s" % schema.email)

    if ClientModel.exists(session, phone=schema.phone):
        raise DatabaseError("Já existe um cliente cadastrado com o telefone: %s" % schema.phone)

    client = ClientModel.create(session, schema)
    streamer.send_event(EventCode.CREATE_USER, context=context, **{"client": client})

    return client


def get_all(session: Session, query: GetClient, context: Context, streamer: Streamer) -> List[ClientModel]:
    return ClientModel.get_all(session, query)


def get_by_id(session: Session, client_id: int, context: Context, streamer: Streamer) -> ClientModel:
    client = ClientModel.get(session, client_id)

    if not client:
        raise NotFoundError(f"Não foi possível localizar o Client com ID: {client_id}")

    return client


def delete(session: Session, client_id: int, context: Context, streamer: Streamer) -> ClientModel:
    client = ClientModel.delete_by_id(session, client_id)

    if not client:
        raise NotFoundError(f"Não foi possível localizar o Client com ID: {client_id}")

    streamer.send_event(event_code=EventCode.DELETE_ITEM, context=context, client=client.dict())

    return client
