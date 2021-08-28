from fastapi import APIRouter
from fastapi.param_functions import Depends
from sqlalchemy.orm.session import Session
from starlette.status import HTTP_201_CREATED

from src.core.crud import item
from src.core.database import make_session
from src.core.schemas import Context, CreateItem, Item
from src.core.services.storage import Storage, default_storage
from src.core.services.streamer import Streamer, default_streamer

router = APIRouter()


@router.get("/{item_id}", response_model=Item)
async def get(item_id: int, session: Session = Depends(make_session), streamer: Streamer = Depends(default_streamer)):
    return item.get_by_id(session, item_id=item_id, context=Context.API, streamer=streamer)


@router.post("/", response_model=Item, status_code=HTTP_201_CREATED)
async def create(
    item: CreateItem,
    fiscal_note_id: int,
    session: Session = Depends(make_session),
    streamer: Streamer = Depends(default_streamer),
    storage: Storage = Depends(default_storage),
):
    return item.create(
        session, item, fiscal_note_id=fiscal_note_id, context=Context.API, streamer=streamer, storage=storage
    )


@router.delete("/{item_id}", response_model=Item)
async def delete(
    item_id: int,
    session: Session = Depends(make_session),
    storage: Storage = Depends(default_storage),
    streamer: Streamer = Depends(default_streamer),
):
    return item.delete(session, item_id, context=Context.API, storage=storage, streamer=streamer)
