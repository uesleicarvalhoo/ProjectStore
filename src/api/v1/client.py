from typing import List

from fastapi import APIRouter
from fastapi.param_functions import Depends
from sqlalchemy.orm import Session
from starlette.status import HTTP_201_CREATED

from src.core.constants import ContextEnum
from src.core.crud import client
from src.core.database import make_session
from src.core.schemas import Client, CreateClient, GetClient
from src.core.services.streamer import Streamer, default_streamer

router = APIRouter()


@router.get("/", response_model=List[Client], response_model_exclude={"password_hash"})
async def get(
    query: GetClient = Depends(),
    session: Session = Depends(make_session),
    streamer: Streamer = Depends(default_streamer),
):
    return client.get_all(session, query, context=ContextEnum.API, streamer=streamer)


@router.get("/{client_id}", response_model=Client)
async def get_by_id(
    client_id: int, session: Session = Depends(make_session), streamer: Streamer = Depends(default_streamer)
):
    return client.get_by_id(session, client_id, context=ContextEnum.API, streamer=streamer)


@router.post("/", response_model=Client, status_code=HTTP_201_CREATED)
async def create(
    schema: CreateClient, session: Session = Depends(make_session), streamer: Streamer = Depends(default_streamer)
):
    return client.create(session, schema, context=ContextEnum.API, streamer=streamer)


@router.delete("/{client_id}", response_model=Client)
async def delete_by_id(
    client_id: int, session: Session = Depends(make_session), streamer: Streamer = Depends(default_streamer)
):
    return client.delete(session, client_id, context=ContextEnum.API, streamer=streamer)
