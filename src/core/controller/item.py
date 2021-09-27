from typing import List
from uuid import uuid4

import inject
from sqlmodel import Session, select

from src.core.events import EventCode
from src.core.exceptions import NotFoundError
from src.core.models import Context, CreateItem, File, FiscalNote, GetItem, Item
from src.core.services import Storage, Streamer
from src.utils.miscellaneous import get_file_hash


@inject.params(streamer=Streamer, storage=Storage)
def create(
    session: Session, schema: CreateItem, fiscal_note_id: int, context: Context, streamer: Streamer, storage: Storage
) -> Item:

    if not session.exec(select(FiscalNote).where(FiscalNote.id == fiscal_note_id)).scalar():
        raise NotFoundError(f"Não foi possível localizar a nota fiscal com id: {fiscal_note_id}.")

    file_hash = get_file_hash(schema.image)
    file = session.exec(select(File).where(File.hash == file_hash)).scalar()

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

    item_obj = Item(**schema.dict(exclude={"image", "filename"}), fiscal_note_id=fiscal_note_id, file=file)

    streamer.send_event(event_code=EventCode.CREATE_ITEM, context=context, item=item_obj.dict())

    return item_obj


def get_all(session: Session, query: GetItem, context: Context) -> List[Item]:
    query_args = []
    if query.id:
        query_args.append(Item.id == query.id)

    elif query.avaliable is not None:
        query_args.append(Item.avaliable == query.avaliable)

    return session.exec(select(Item).where(*query_args)).scalars()


def get_by_id(session: Session, item_id: int, context: Context) -> Item:
    item = session.exec(select(Item).where(Item.id == item_id)).scalar()

    if not item:
        raise NotFoundError("Não foi possível localizar o Item com ID: %s" % item_id)

    return item


@inject.params(streamer=Streamer)
def delete(session: Session, item_id: int, context: Context, streamer: Streamer) -> Item:
    item = session.exec(select(Item).where(Item.id == item_id)).scalar()

    if not item:
        raise NotFoundError(f"Não foi possível localizar o item com ID {item_id}")

    session.delete(item)
    session.commit()
    streamer.send_event(EventCode.DELETE_ITEM, context=context, item=item.dict())

    return item
