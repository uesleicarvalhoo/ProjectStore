from typing import List
from uuid import UUID

from fastapi import APIRouter
from fastapi.param_functions import Depends
from sqlalchemy.orm.session import Session
from starlette.status import HTTP_201_CREATED

from src.core.controller import item
from src.core.helpers.database import make_session
from src.core.models import Context, CreateItem, Item, QueryItem
from src.utils.dependencies import api_context_manager

router = APIRouter()


@router.get("/", response_model=List[Item])
async def get_all(
    query: QueryItem = Depends(),
    session: Session = Depends(make_session),
    context: Context = Depends(api_context_manager),
):
    return item.get_all(session, query, context=context)


@router.get("/{item_id}", response_model=Item)
async def get(item_id: UUID, session: Session = Depends(make_session), context: Context = Depends(api_context_manager)):
    return item.get_by_id(session, item_id=item_id, context=context)


@router.post("/", response_model=Item, status_code=HTTP_201_CREATED)
async def create(
    item: CreateItem,
    fiscal_note_id: UUID,
    session: Session = Depends(make_session),
    context: Context = Depends(api_context_manager),
):
    return item.create(session, item, fiscal_note_id=fiscal_note_id, context=context)


@router.delete("/{item_id}", response_model=Item)
async def delete(
    item_id: UUID, session: Session = Depends(make_session), context: Context = Depends(api_context_manager)
):
    return item.delete(session, item_id, context=context)
