from typing import List
from uuid import UUID, uuid4

import inject
from sqlmodel import Session, select

from src.core.events import EventCode
from src.core.helpers.exceptions import NotFoundError
from src.core.models import Context, CreateItem, File, FiscalNote, Item, QueryItem
from src.core.services import Storage, Streamer
from src.utils.miscellaneous import get_file_hash


@inject.params(streamer=Streamer, storage=Storage)
def create(
    session: Session, schema: CreateItem, fiscal_note_id: UUID, context: Context, streamer: Streamer, storage: Storage
) -> Item:

    if not session.exec(select(FiscalNote).where(FiscalNote.id == fiscal_note_id)).first():
        raise NotFoundError(f"Não foi possível localizar a nota fiscal com id: {fiscal_note_id}.")

    file_hash = get_file_hash(schema.image)
    file = session.exec(select(File).where(File.hash == file_hash)).first()

    if not file:
        streamer.send_event(
            EventCode.UPLOAD_FILE, context=context, file={"filename": schema.filename, "hash": file_hash}
        )
        file = File(bucket_key=f"item-{uuid4()}.{schema.file_extension}", hash=file_hash)

    if not storage.check_file_exists(file.bucket_key):
        storage.upload_file(schema.image, key=file.bucket_key)
        streamer.send_event(
            EventCode.UPLOAD_FILE,
            context=context,
            file={"filename": schema.filename, "hash": file_hash, "bucket_key": file.bucket_key},
        )

    item_obj = Item(**schema.dict(exclude={"image": ..., "filename": ...}), fiscal_note_id=fiscal_note_id, file=file)
    session.add(item_obj)
    session.commit()

    streamer.send_event(event_code=EventCode.CREATE_ITEM, context=context, item=item_obj.dict())

    return item_obj


def get_all(session: Session, query_schema: QueryItem, context: Context) -> List[Item]:
    query = select(Item)

    if query_schema.avaliable is not None:
        query = query.where(Item.avaliable == query_schema.avaliable)

    query = query.offset(query_schema.offset)

    if query_schema.limit > 0:
        query = query.limit(query_schema.limit)

    return session.exec(query).all()


def get_by_id(session: Session, item_id: UUID, context: Context) -> Item:
    item = session.exec(select(Item).where(Item.id == item_id)).first()

    if not item:
        raise NotFoundError("Não foi possível localizar o Item com ID: %s" % item_id)

    return item


@inject.params(streamer=Streamer)
def delete(session: Session, item_id: UUID, context: Context, streamer: Streamer) -> Item:
    item = session.exec(select(Item).where(Item.id == item_id)).first()

    if not item:
        raise NotFoundError(f"Não foi possível localizar o item com ID {item_id}")

    session.delete(item)
    session.commit()
    streamer.send_event(EventCode.DELETE_ITEM, context=context, item=item.dict())

    return item
