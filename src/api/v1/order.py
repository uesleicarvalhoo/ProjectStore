from typing import List

from fastapi import APIRouter
from fastapi.param_functions import Depends
from sqlalchemy.orm import Session
from starlette.status import HTTP_201_CREATED

from src.core.crud import order
from src.core.database import make_session
from src.core.schemas import Context, CreateOrder, GetOrder, Order

router = APIRouter()


@router.get("/", response_model=List[Order])
async def get_all(query: GetOrder = Depends(), session: Session = Depends(make_session)):
    return order.get_all(session, query, context=Context.API)


@router.get("/{order_id}", response_model=Order)
async def get(order_id: int, session: Session = Depends(make_session)):
    return order.get_by_id(session, order_id, context=Context.API)


@router.post("/", response_model=Order, status_code=HTTP_201_CREATED)
async def create(schema: CreateOrder, session: Session = Depends(make_session)):
    return order.create(session, schema, context=Context.API)
