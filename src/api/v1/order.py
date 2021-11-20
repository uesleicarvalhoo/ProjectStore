from typing import List
from uuid import UUID

from fastapi import APIRouter
from fastapi.param_functions import Depends
from sqlmodel import Session
from starlette.status import HTTP_201_CREATED

from src.core.controller import order
from src.core.helpers.database import make_session
from src.core.models import Context, CreateOrder, Order, QueryOrder
from src.core.models.order import OrderResponse
from src.utils.dependencies import context_manager

router = APIRouter()


@router.get("/", response_model=List[OrderResponse])
async def get_all(
    query: QueryOrder = Depends(),
    session: Session = Depends(make_session),
    context: Context = Depends(context_manager),
):
    return order.get_all(session, query, context=context)


@router.get("/{order_id}", response_model=Order)
async def get(order_id: UUID, session: Session = Depends(make_session), context: Context = Depends(context_manager)):
    return order.get_by_id(session, order_id, context=context)


@router.post("/", response_model=Order, status_code=HTTP_201_CREATED)
async def create(
    schema: CreateOrder, session: Session = Depends(make_session), context: Context = Depends(context_manager)
):
    return order.register_sale(session, schema, context=context)


@router.delete("/{order_id}", response_model=Order)
async def delete(order_id: UUID, session: Session = Depends(make_session), context: Context = Depends(context_manager)):
    return order.delete_by_id(session, order_id, context=context)
