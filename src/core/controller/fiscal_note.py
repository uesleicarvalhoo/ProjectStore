from typing import List, Union
from uuid import UUID, uuid4

import inject
from sqlmodel import Session, select

from src.core.events import EventCode
from src.core.helpers.exceptions import NotFoundError
from src.core.models import Context, CreateFiscalNote, File, FiscalNote, Item, QueryFiscalNote
from src.core.services import Storage, Streamer
from src.utils.miscellaneous import get_file_hash


@inject.params(streamer=Streamer, storage=Storage)
def create(session: Session, schema: CreateFiscalNote, context: Context, streamer: Streamer, storage: Storage):
    def get_or_create_file(file: Union[str, bytes], preffix: str, extension: str) -> File:
        file_hash = get_file_hash(file)
        file = session.exec(select(File).where(File.hash == file_hash)).first()

        if not file:
            file = File(bucket_key=f"{preffix}-{uuid4()}.{extension}", hash=file_hash)
            session.add(file)

        return file

    file = get_or_create_file(schema.image, "fiscal-note", schema.file_extension)

    if not storage.check_file_exists(file.bucket_key):
        storage.upload_file(schema.image, key=file.bucket_key)
        streamer.send_event(
            EventCode.UPLOAD_FILE, context=context, file={"filename": schema.filename, "hash": file.hash}
        )

    fiscal_note = FiscalNote(
        **schema.dict(exclude={"image": ..., "filename": ..., "items": ...}), file_id=file.bucket_key
    )
    session.add(fiscal_note)

    for item in schema.items:
        file = get_or_create_file(item.image, "item", item.file_extension)
        item_obj = Item(
            **item.dict(exclude={"image": ..., "filename": ...}), fiscal_note_id=fiscal_note.id, file_id=file.bucket_key
        )
        session.add(item_obj)

    session.commit()
    streamer.send_event(event_code=EventCode.CREATE_FISCAL_NOTE, context=context, fiscal_note=fiscal_note.dict())

    return fiscal_note


def get_all(session: Session, query_schema: QueryFiscalNote, context: Context) -> List[FiscalNote]:
    query = select(FiscalNote).offset(query_schema.offset)

    if query_schema.limit > 0:
        query = query.limit(query_schema.limit)

    return session.exec(query).all()


@inject.params(storage=Storage)
def get_by_id(session: Session, fiscal_note_id: UUID, context: Context, storage: Storage) -> FiscalNote:
    fiscal_note = session.exec(select(FiscalNote).where(FiscalNote.id == fiscal_note_id)).first()

    if not fiscal_note:
        raise NotFoundError(f"Não foi possível localizar a nota fiscal com ID {fiscal_note_id}")

    if not fiscal_note.file or not storage.check_file_exists(fiscal_note.file.bucket_key):
        raise NotFoundError(f"Não foi possível localizar o arquivo da nota fiscal {fiscal_note_id}")

    return fiscal_note


@inject.params(streamer=Streamer)
def delete(session: Session, fiscal_note_id: UUID, context: Context, streamer: Streamer) -> FiscalNote:
    fiscal_note = session.exec(select(FiscalNote).where(FiscalNote.id == fiscal_note_id)).first()

    if not fiscal_note:
        raise NotFoundError(f"Não foi possível localizar a nota fiscal com ID: {fiscal_note_id}")

    session.delete(fiscal_note)
    session.commit()

    streamer.send_event(EventCode.DELETE_FISCAL_NOTE, context=context, fiscal_note=fiscal_note.dict())

    return fiscal_note
