from uuid import uuid4

from fastapi import APIRouter
from fastapi.exceptions import HTTPException
from fastapi.param_functions import Depends
from sqlalchemy.orm.session import Session
from starlette.status import HTTP_201_CREATED, HTTP_204_NO_CONTENT

from src.core.database.helpers import master_session, read_session
from src.core.database.models import File as FileModel
from src.core.database.models import FiscalNote as FiscalNoteModel
from src.core.database.models import Item as ItemModel
from src.core.events import EventCode
from src.core.exceptions import NotFoundError
from src.core.schemas import CreateFile, CreateItem, Item
from src.core.services.storage import Storage, default_storage
from src.core.services.streamer import Streamer, default_streamer
from src.utils.file import get_file_hash

router = APIRouter()


@router.get("/{item_id}", response_model=Item)
async def get(item_id: int, session: Session = Depends(read_session)):
    item = ItemModel.get(session, item_id)

    if not item:
        raise NotFoundError(f"Não foi possível localizar o item com o ID {item_id}.")

    return item


@router.post("/", response_model=Item, status_code=HTTP_201_CREATED)
async def create(
    item: CreateItem,
    fiscal_note_id: int,
    session: Session = Depends(master_session),
    streamer: Streamer = Depends(default_streamer),
    storage: Storage = Depends(default_storage),
):

    if not FiscalNoteModel.get(session, fiscal_note_id):
        raise NotFoundError(f"Não foi possível localizar a nota fiscal com id: {fiscal_note_id}.")

    file_hash = get_file_hash(item.image)
    file = FileModel.get_by_hash(session, file_hash)

    if not file:
        streamer.send_event(EventCode.UPLOAD_FILE, file={"filename": item.filename, "hash": file_hash})
        file = FileModel.create(
            session,
            CreateFile(bucket_key=f"item-{uuid4()}.{item.filename.split('.')[-1]}", hash=file_hash),
        )

    if not storage.check_file_exists(file.bucket_key):
        storage.upload_file(item.image, key=file.bucket_key)
        streamer.send_event(
            EventCode.UPLOAD_FILE, file={"filename": item.filename, "hash": file_hash, "bucket_key": file.bucket_key}
        )

    item_obj = ItemModel.create(session, item, fiscal_note_id=fiscal_note_id, file=file)

    streamer.send_event(event_code=EventCode.CREATE_ITEM, item=item_obj.dict())

    return item_obj


@router.delete("/{item_id}", response_model=Item)
async def delete(
    item_id: int,
    session: Session = Depends(master_session),
    storage: Storage = Depends(default_storage),
    streamer: Streamer = Depends(default_streamer),
):
    item = ItemModel.delete_by_id(session, item_id)

    if not item:
        raise HTTPException(HTTP_204_NO_CONTENT, f"Não foi possível localizar o item com ID {item_id}")

    streamer.send_event(EventCode.DELETE_ITEM, item=item.dict())

    return item
