from typing import List
from uuid import uuid4

import inject
from sqlalchemy.orm import Session

from src.core.database.models import File as FileModel
from src.core.database.models import FiscalNote as FiscalNoteModel
from src.core.database.models import Item as ItemModel
from src.core.events import EventCode
from src.core.exceptions import NotFoundError
from src.core.schemas import Context, CreateFile, CreateItem, GetItem
from src.core.services import Storage, Streamer
from src.utils.miscellaneous import get_file_hash


@inject.params(streamer=Streamer, storage=Storage)
def create(
    session: Session, item: CreateItem, fiscal_note_id: int, context: Context, streamer: Streamer, storage: Storage
) -> ItemModel:
    if not FiscalNoteModel.get(session, fiscal_note_id):
        raise NotFoundError(f"Não foi possível localizar a nota fiscal com id: {fiscal_note_id}.")

    file_hash = get_file_hash(item.image)
    file = FileModel.get_by_hash(session, file_hash)

    if not file:
        streamer.send_event(EventCode.UPLOAD_FILE, context=context, file={"filename": item.filename, "hash": file_hash})
        file = FileModel.create(
            session,
            CreateFile(bucket_key=f"item-{uuid4()}.{item.filename.split('.')[-1]}", hash=file_hash),
        )

    if not storage.check_file_exists(file.bucket_key):
        storage.upload_file(item.image, key=file.bucket_key)
        streamer.send_event(
            EventCode.UPLOAD_FILE,
            context=context,
            file={"filename": item.filename, "hash": file_hash, "bucket_key": file.bucket_key},
        )

    item_obj = ItemModel.create(session, item, fiscal_note_id=fiscal_note_id, file=file)

    streamer.send_event(event_code=EventCode.CREATE_ITEM, context=context, item=item_obj.dict())

    return item_obj


def get_all(session: Session, query: GetItem, context: Context) -> List[ItemModel]:
    return ItemModel.get_all(session, query)


def get_by_id(session: Session, item_id: int, context: Context) -> ItemModel:
    item = ItemModel.get(session, item_id)

    if not item:
        raise NotFoundError("Não foi possível localizar o Item com ID: %s" % item_id)

    return item


@inject.params(streamer=Streamer)
def delete(session: Session, item_id: int, context: Context, streamer: Streamer) -> ItemModel:
    item = ItemModel.delete_by_id(session, item_id)

    if not item:
        raise NotFoundError(f"Não foi possível localizar o item com ID {item_id}")

    streamer.send_event(EventCode.DELETE_ITEM, context=context, item=item.dict())

    return item
