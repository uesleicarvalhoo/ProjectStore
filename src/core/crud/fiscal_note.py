from typing import List
from uuid import uuid4

import inject
from sqlalchemy.orm import Session

from src.core.database.models import File as FileModel
from src.core.database.models import FiscalNote as FiscalNoteModel
from src.core.database.models import Item as ItemModel
from src.core.events import EventCode
from src.core.exceptions import NotFoundError
from src.core.schemas import Context, CreateFile, CreateFiscalNote, GetFiscalNote
from src.core.services import Storage, Streamer
from src.utils.miscellaneous import get_file_hash


@inject.params(streamer=Streamer, storage=Storage)
def create(session: Session, schema: CreateFiscalNote, context: Context, streamer: Streamer, storage: Storage):
    file_hash = get_file_hash(schema.image)
    file = FileModel.get_by_hash(session, file_hash)

    if not file:
        file = FileModel.create(
            session,
            CreateFile(bucket_key=f"fiscal-note-{uuid4()}.{schema.filename.split('.')[-1]}", hash=file_hash),
        )

    if not storage.check_file_exists(file.bucket_key):
        storage.upload_file(schema.image, key=file.bucket_key)
        streamer.send_event(
            EventCode.UPLOAD_FILE, context=context, file={"filename": schema.filename, "hash": file_hash}
        )

    fiscal_note = FiscalNoteModel.create(session, schema, file=file)

    for item in schema.items:
        file_hash = get_file_hash(item.image)
        file = FileModel.get_by_hash(session, file_hash)

        if not file:
            file = FileModel.create(
                session,
                CreateFile(bucket_key=f"item-{uuid4()}.{item.filename.split('.')[-1]}", hash=file_hash),
            )

        ItemModel.create(session, item, fiscal_note.id, file)

    streamer.send_event(event_code=EventCode.CREATE_FISCAL_NOTE, context=context, fiscal_note=fiscal_note.dict())

    return fiscal_note


def get_all(session: Session, query: GetFiscalNote, context: Context) -> List[FiscalNoteModel]:
    return FiscalNoteModel.get_all(session, query)


@inject.params(storage=Storage)
def get_by_id(session: Session, fiscal_note_id: int, context: Context, storage: Storage) -> FiscalNoteModel:
    fiscal_note = FiscalNoteModel.get(session, fiscal_note_id)

    if not fiscal_note:
        raise NotFoundError(f"Não foi possível localizar a nota fiscal com ID {fiscal_note_id}")

    if not fiscal_note.file or not storage.check_file_exists(fiscal_note.file.bucket_key):
        raise NotFoundError(f"Não foi possível localizar o arquivo da nota fiscal {fiscal_note_id}")

    return fiscal_note


@inject.params(streamer=Streamer)
def delete(session: Session, fiscal_note_id: int, context: Context, streamer: Streamer) -> FiscalNoteModel:
    fiscal_note = FiscalNoteModel.delete_by_id(session, fiscal_note_id)

    if not fiscal_note:
        raise NotFoundError(f"Não foi possível localizar a nota fiscal com ID: {fiscal_note_id}")

    streamer.send_event(EventCode.DELETE_FISCAL_NOTE, context=context, fiscal_note=fiscal_note.dict())

    return fiscal_note
