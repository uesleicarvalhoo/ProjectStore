from typing import List
from uuid import UUID

import inject
from sqlmodel import Session, select

from src.core.events import EventDescription
from src.core.helpers.exceptions import NotAuthorizedError, NotFoundError
from src.core.models import Context, CreateFiscalNoteItem, CreateItem, FiscalNote, FiscalNoteItem, QueryFiscalNote
from src.core.services import Streamer

from . import file, item


@inject.params(streamer=Streamer)
def create(
    session: Session,
    schema: CreateFiscalNoteItem,
    fiscal_note_id: UUID,
    context: Context,
    streamer: Streamer,
) -> FiscalNoteItem:

    if not session.exec(select(FiscalNote).where(FiscalNote.id == fiscal_note_id)).first():
        raise NotFoundError(f"Não foi possível localizar a nota fiscal com id: {fiscal_note_id}.")

    file_obj = file.get_or_create_file(session, "fiscal-note-item", schema.filename, schema.image, context=context)
    item_obj = item.create(
        session,
        schema=CreateItem(
            code=schema.code, name=schema.name, cost=schema.buy_value, value=schema.sugested_sell_value, amount=1
        ),
        context=context,
    )

    fiscal_note_item_obj = FiscalNoteItem(
        **schema.dict(exclude={"image": ..., "filename": ..., "name": ..., "code": ...}),
        fiscal_note_id=fiscal_note_id,
        item_id=item_obj.id,
        file_id=file_obj.bucket_key,
        owner_id=context.user_id,
    )

    session.add(item_obj)
    session.add(fiscal_note_item_obj)
    session.commit()

    streamer.send_event(description=EventDescription.CREATE_ITEM, context=context, item=fiscal_note_item_obj.dict())

    return fiscal_note_item_obj


def get_all(session: Session, query_schema: QueryFiscalNote, context: Context) -> List[FiscalNoteItem]:
    args = []

    if not context.user_is_super_user:
        args.append(FiscalNoteItem.owner_id == context.user_id)

    return session.exec(select(FiscalNoteItem).where(*args)).all()


def get_by_id(session: Session, item_id: UUID, context: Context) -> FiscalNoteItem:
    item = session.exec(select(FiscalNoteItem).where(FiscalNoteItem.id == item_id)).first()

    if not item:
        raise NotFoundError("Não foi possível localizar o Item com ID: %s" % item_id)

    if not context.user_is_super_user and item.owner_id != context.user_id:
        raise NotAuthorizedError(f"Você não possui permissão para consultar o FiscalNoteItem {item_id}")

    return item


@inject.params(streamer=Streamer)
def delete(session: Session, item_id: UUID, context: Context, streamer: Streamer) -> FiscalNoteItem:
    item = session.exec(select(FiscalNoteItem).where(FiscalNoteItem.id == item_id)).first()

    if not item:
        raise NotFoundError(f"Não foi possível localizar o item com ID {item_id}")

    if not context.user_is_super_user and item.owner_id != context.user_id:
        raise NotAuthorizedError(f"Você não possui permissão para excluir o FiscalNoteItem {item_id}")

    session.delete(item)
    session.commit()
    streamer.send_event(EventDescription.DELETE_ITEM, context=context, item=item.dict())

    return item
