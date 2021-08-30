from typing import List

from fastapi import APIRouter
from fastapi.param_functions import Depends
from sqlalchemy.orm import Session
from starlette.status import HTTP_201_CREATED

from src.core.constants import ContextEnum
from src.core.crud import client
from src.core.database import make_session
from src.core.schemas import Client, CreateClient, GetClient

router = APIRouter()


@router.get("/", response_model=List[Client], response_model_exclude={"password_hash"})
async def get(query: GetClient = Depends(), session: Session = Depends(make_session)):
    return client.get_all(session, query, context=ContextEnum.API)


@router.get("/{client_id}", response_model=Client)
async def get_by_id(client_id: int, session: Session = Depends(make_session)):
    return client.get_by_id(session, client_id, context=ContextEnum.API)


@router.post("/", response_model=Client, status_code=HTTP_201_CREATED)
async def create(schema: CreateClient, session: Session = Depends(make_session)):
    return client.create(session, schema, context=ContextEnum.API)


@router.delete("/{client_id}", response_model=Client)
async def delete_by_id(client_id: int, session: Session = Depends(make_session)):
    return client.delete(session, client_id, context=ContextEnum.API)
