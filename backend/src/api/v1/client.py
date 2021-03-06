from typing import List
from uuid import UUID

from fastapi import APIRouter
from fastapi.param_functions import Depends
from sqlmodel import Session
from starlette.status import HTTP_201_CREATED

from src.core.controller import client
from src.core.helpers.database import make_session
from src.core.models import Client, Context, CreateClient, QueryClient, UpdateClient
from src.utils.dependencies import context_manager

router = APIRouter()


@router.get("/", response_model=List[Client])
async def get(
    query: QueryClient = Depends(),
    session: Session = Depends(make_session),
    context: Context = Depends(context_manager),
):
    return client.get_all(session, query, context)


@router.get("/{client_id}", response_model=Client)
async def get_by_id(
    client_id: UUID, session: Session = Depends(make_session), context: Context = Depends(context_manager)
):
    return client.get_by_id(session, client_id, context=context)


@router.patch("/")
async def update(
    data: UpdateClient, session: Session = Depends(make_session), context: Context = Depends(context_manager)
):
    return client.update(session, data, context=context)


@router.post("/", response_model=Client, status_code=HTTP_201_CREATED)
async def create(
    schema: CreateClient, session: Session = Depends(make_session), context: Context = Depends(context_manager)
):
    return client.create(session, schema, context=context)


@router.delete("/{client_id}", response_model=Client)
async def delete_by_id(
    client_id: UUID, session: Session = Depends(make_session), context: Context = Depends(context_manager)
):
    return client.delete(session, client_id, context=context)
