from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette.status import HTTP_201_CREATED

from src.core.crud import fiscal_note
from src.core.database import make_session
from src.core.schemas import Context, CreateFiscalNote, FiscalNote

router = APIRouter()


@router.get("/{fiscal_note_id}", response_model=FiscalNote)
async def get(fiscal_note_id: int, session: Session = Depends(make_session)):
    return fiscal_note.get_by_id(session, fiscal_note_id, context=Context.API)


@router.post("/", response_model=FiscalNote, status_code=HTTP_201_CREATED)
async def create(schema: CreateFiscalNote, session: Session = Depends(make_session)):
    return fiscal_note.create(session, schema, context=Context.API)
