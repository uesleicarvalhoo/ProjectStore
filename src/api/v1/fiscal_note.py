from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette.status import HTTP_201_CREATED

from src.core.crud import fiscal_note
from src.core.database import make_session
from src.core.schemas import Context, CreateFiscalNote, FiscalNote
from src.core.services.storage import Storage, default_storage
from src.core.services.streamer import Streamer, default_streamer

router = APIRouter()


@router.get("/{fiscal_note_id}", response_model=FiscalNote)
async def get(
    fiscal_note_id: int,
    session: Session = Depends(make_session),
    storage: Storage = Depends(default_storage),
    streamer: Streamer = Depends(default_streamer),
):
    return fiscal_note.get_by_id(session, fiscal_note_id, context=Context.API, streamer=streamer, storage=storage)


@router.post("/", response_model=FiscalNote, status_code=HTTP_201_CREATED)
async def create(
    schema: CreateFiscalNote,
    session: Session = Depends(make_session),
    streamer: Streamer = Depends(default_streamer),
    storage: Storage = Depends(default_storage),
):
    return fiscal_note.create(session, schema, context=Context.API, streamer=streamer, storage=storage)
