from typing import List
from uuid import UUID

import inject
from sqlmodel import Session, select

from src.core.events import EventDescription
from src.core.helpers.exceptions import NotAuthorizedError, NotFoundError
from src.core.models import Context, CreateItem, Item, QueryItem, UpdateItem
from src.core.services import Streamer


@inject.params(streamer=Streamer)
def create(session: Session, schema: CreateItem, context: Context, streamer: Streamer) -> Item:

    item = Item(
        **schema.dict(exclude={"image": ..., "filename": ...}),
        owner_id=context.user_id,
    )

    session.add(item)
    session.commit()

    streamer.send_event(description=EventDescription.CREATE_ITEM, context=context, item=item.dict())

    return item


def get_all(session: Session, query_schema: QueryItem, context: Context) -> List[Item]:
    args = []

    if not context.user_is_super_user and context.user_id:
        args.append(Item.owner_id == context.user_id)

    if query_schema.avaliable is not None:
        args.append(Item.amount >= 1 if query_schema.avaliable else Item.amount < 1)

    return session.exec(select(Item).where(*args)).all()


def get_by_id(session: Session, item_id: UUID, context: Context) -> Item:
    item = session.exec(select(Item).where(Item.id == item_id)).first()

    if not item:
        raise NotFoundError("Não foi possível localizar o Item com ID: %s" % item_id)

    if not context.user_is_super_user and item.owner_id != context.user_id:
        raise NotAuthorizedError(f"Você não possui permissão para consultar o Item {item_id}")

    return item


@inject.params(streamer=Streamer)
def update(session: Session, data: UpdateItem, context: Context, streamer: Streamer) -> Item:
    item = session.exec(select(Item).where(Item.id == data.id)).first()

    if not item:
        raise NotFoundError(f"Não foi possível localizar o Produto com ID: {data.id}")

    if not context.user_is_super_user and item.owner_id != context.user_id:
        raise NotAuthorizedError(f'Você não possui permissão para editar o Produto: "{item.name}"')

    columns = item.__table__.columns.keys()

    for key, value in data:
        if key not in columns:
            continue

        setattr(item, key, value)

    session.add(item)
    session.commit()

    streamer.send_event(
        description=EventDescription.UPDATE_ITEM,
        context=context,
        data={"item_data": item.dict(), "update_schema": data.dict()},
    )
    return item


@inject.params(streamer=Streamer)
def delete(session: Session, item_id: UUID, context: Context, streamer: Streamer) -> Item:
    item = session.exec(select(Item).where(Item.id == item_id)).first()

    if not item:
        raise NotFoundError(f"Não foi possível localizar o item com ID {item_id}")

    if not context.user_is_super_user and item.owner_id != context.user_id:
        raise NotAuthorizedError(f"Você não possui permissão para excluir o Item {item_id}")

    session.delete(item)
    session.commit()
    streamer.send_event(EventDescription.DELETE_ITEM, context=context, item=item.dict())

    return item
