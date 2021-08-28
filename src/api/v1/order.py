from typing import List

from fastapi import APIRouter
from fastapi.param_functions import Depends
from sqlalchemy.orm import Session
from starlette.status import HTTP_201_CREATED

from src.core.crud import order
from src.core.database import make_session
from src.core.schemas import Context, CreateOrder, GetOrder, Order
from src.core.services.streamer import Streamer, default_streamer

router = APIRouter()


@router.get("/", response_model=List[Order])
async def get_all(
    query: GetOrder = Depends(),
    session: Session = Depends(make_session),
    streamer: Streamer = Depends(default_streamer),
):
    return order.get_all(session, query, context=Context.API, streamer=streamer)


@router.get("/{order_id}", response_model=Order)
async def get(order_id: int, session: Session = Depends(make_session), streamer: Streamer = Depends(default_streamer)):
    return order.get_by_id(session, order_id, context=Context.API, streamer=streamer)


@router.post("/", response_model=Order, status_code=HTTP_201_CREATED)
async def create(
    schema: CreateOrder, session: Session = Depends(make_session), streamer: Streamer = Depends(default_streamer)
):
    return order.create(session, schema, context=Context.API, streamer=streamer)
