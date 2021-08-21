from typing import List

from fastapi import APIRouter
from fastapi.param_functions import Depends
from sqlalchemy.orm import Session
from starlette.exceptions import HTTPException
from starlette.status import HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_400_BAD_REQUEST

from src.core.database.helpers import master_session, read_session
from src.core.database.models import Client as ClientModel
from src.core.events import EventCode
from src.core.exceptions import NotFoundError
from src.core.schemas import Client, CreateClient, GetClient
from src.core.services.streamer import Streamer, default_streamer

router = APIRouter()


@router.get("/", response_model=List[Client], response_model_exclude={"password_hash"})
async def get(query: GetClient = Depends(), session: Session = Depends(read_session)):
    return ClientModel.get_all(session, query)


@router.get("/{client_id}", response_model=Client)
async def get_by_id(client_id, session: Session = Depends(read_session)):
    client = ClientModel.get(session, client_id)

    if not client:
        raise NotFoundError(f"Not found client with id: {client_id}")

    return client


@router.post("/", response_model=Client, status_code=HTTP_201_CREATED)
async def create(
    schema: CreateClient, session: Session = Depends(master_session), streamer: Streamer = Depends(default_streamer)
):

    if ClientModel.exists(session, email=schema.email):
        raise HTTPException(HTTP_400_BAD_REQUEST, "Já existe um cliente cadastrado com o email: %s" % schema.email)

    if ClientModel.exists(session, phone=schema.phone):
        raise HTTPException(HTTP_400_BAD_REQUEST, "Já existe um cliente cadastrado com o telefone: %s" % schema.phone)

    client = ClientModel.create(session, schema)
    streamer.send_event(EventCode.CREATE_USER, **{"client": client})

    return client


@router.delete("/{client_id}", response_model=Client)
async def delete_by_id(
    client_id: int, session: Session = Depends(master_session), streamer: Streamer = Depends(default_streamer)
):
    client = ClientModel.delete_by_id(session, client_id)

    if not client:
        raise HTTPException(HTTP_204_NO_CONTENT, {f"Not found client with id: {client_id}"})

    streamer.send_event(event_code=EventCode.DELETE_ITEM, client=client.dict())

    return client
