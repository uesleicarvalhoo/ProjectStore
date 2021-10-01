from uuid import UUID

from fastapi import APIRouter, Depends
from sqlmodel import Session
from starlette.status import HTTP_201_CREATED

from src.core.controller import fiscal_note
from src.core.helpers.database import make_session
from src.core.models import Context, CreateFiscalNote, FiscalNote

router = APIRouter()


@router.get("/{fiscal_note_id}", response_model=FiscalNote)
async def get(fiscal_note_id: UUID, session: Session = Depends(make_session)):
    return fiscal_note.get_by_id(session, fiscal_note_id, context=Context.API)


@router.post("/", response_model=FiscalNote, status_code=HTTP_201_CREATED)
async def create(schema: CreateFiscalNote, session: Session = Depends(make_session)):
    return fiscal_note.create(session, schema, context=Context.API)
