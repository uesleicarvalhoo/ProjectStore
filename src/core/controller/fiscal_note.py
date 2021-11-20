from typing import List
from uuid import UUID

import inject
from sqlmodel import Session, select

from src.core.events import EventDescription
from src.core.helpers.exceptions import NotAuthorizedError, NotFoundError
from src.core.models import Context, CreateFiscalNote, FiscalNote, QueryFiscalNote
from src.core.services import Streamer

from . import file, fiscal_note_item


@inject.params(streamer=Streamer)
def create(session: Session, schema: CreateFiscalNote, context: Context, streamer: Streamer):
    file_obj = file.get_or_create_file(session, "fiscal-note", schema.filename, schema.image, context=context)

    fiscal_note = FiscalNote(
        **schema.dict(exclude={"image": ..., "filename": ..., "items": ...}),
        file_id=file_obj.bucket_key,
        owner_id=context.user_id,
    )
    session.add(fiscal_note)

    for item in schema.items:
        item_obj = fiscal_note_item.create(
            session,
            schema=item,
            fiscal_note_id=fiscal_note.id,
            context=context,
        )
        session.add(item_obj)

    session.commit()
    streamer.send_event(
        description=EventDescription.CREATE_FISCAL_NOTE, context=context, fiscal_note=fiscal_note.dict()
    )

    return fiscal_note


def get_all(session: Session, query_schema: QueryFiscalNote, context: Context) -> List[FiscalNote]:
    args = []

    if not context.user_is_super_user:
        args.append(FiscalNote.owner_id == context.user_id)

    return session.exec(select(FiscalNote).where(*args)).all()


def get_by_id(session: Session, fiscal_note_id: UUID, context: Context) -> FiscalNote:
    fiscal_note = session.exec(select(FiscalNote).where(FiscalNote.id == fiscal_note_id)).first()

    if not fiscal_note:
        raise NotFoundError(f"Não foi possível localizar a nota fiscal com ID {fiscal_note_id}")

    if not context.user_is_super_user and fiscal_note.owner_id != context.user_id:
        raise NotAuthorizedError(f"Você não possui permissão para consultar os dados da Nota Fiscal {fiscal_note_id}!")

    if not fiscal_note.file or not file.check_file_exists(fiscal_note.file.bucket_key):
        raise NotFoundError(f"Não foi possível localizar o arquivo da nota fiscal {fiscal_note_id}")

    return fiscal_note


@inject.params(streamer=Streamer)
def delete(session: Session, fiscal_note_id: UUID, context: Context, streamer: Streamer) -> FiscalNote:
    fiscal_note = session.exec(select(FiscalNote).where(FiscalNote.id == fiscal_note_id)).first()

    if not fiscal_note:
        raise NotFoundError(f"Não foi possível localizar a Nota Fiscal com ID: {fiscal_note_id}")

    if not context.user_is_super_user and fiscal_note.owner_id != context.user_id:
        raise NotAuthorizedError(f"Você não possui permissão para exlcuir a Nota Fiscal {fiscal_note_id}!")

    session.delete(fiscal_note)
    session.commit()

    streamer.send_event(EventDescription.DELETE_FISCAL_NOTE, context=context, fiscal_note=fiscal_note.dict())

    return fiscal_note
