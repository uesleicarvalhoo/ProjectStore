from uuid import uuid4

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette.status import HTTP_201_CREATED

from src.core.database.helpers import master_session, read_session
from src.core.database.models import File as FileModel
from src.core.database.models import FiscalNote as FiscalNoteModel
from src.core.database.models import Item as ItemModel
from src.core.events import EventCode
from src.core.exceptions import NotFoundError
from src.core.schemas import CreateFile, CreateFiscalNote, FiscalNote
from src.core.services.storage import Storage, default_storage
from src.core.services.streamer import Streamer, default_streamer
from src.utils.file import get_file_hash

router = APIRouter()


@router.get("/{fiscal_note_id}", response_model=FiscalNote)
async def get(
    fiscal_note_id: int, session: Session = Depends(read_session), storage: Storage = Depends(default_storage)
):
    fiscal_note = FiscalNoteModel.get(session, fiscal_note_id)

    if not fiscal_note:
        raise NotFoundError(f"Não foi possível localizar a nota fiscal com ID {fiscal_note_id}")

    if not fiscal_note.file or not storage.check_file_exists(fiscal_note.file.bucket_key):
        raise NotFoundError(f"Não foi possível localizar o arquivo da nota fiscal {fiscal_note_id}")

    return fiscal_note


@router.post("/", response_model=FiscalNote, status_code=HTTP_201_CREATED)
async def upload(
    schema: CreateFiscalNote,
    session: Session = Depends(master_session),
    streamer: Streamer = Depends(default_streamer),
    storage: Storage = Depends(default_storage),
):

    file_hash = get_file_hash(schema.image)
    file = FileModel.get_by_hash(session, file_hash)

    if not file:
        file = FileModel.create(
            session,
            CreateFile(bucket_key=f"fiscal-note-{uuid4()}.{schema.filename.split('.')[-1]}", hash=file_hash),
        )

    if not storage.check_file_exists(file.bucket_key):
        storage.upload_file(schema.image, key=file.bucket_key)
        streamer.send_event(EventCode.UPLOAD_FILE, file={"filename": schema.filename, "hash": file_hash})

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

    streamer.send_event(event_code=EventCode.CREATE_FISCAL_NOTE, fiscal_note=fiscal_note.dict())

    return fiscal_note
