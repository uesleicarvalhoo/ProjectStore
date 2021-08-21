from typing import List

from fastapi import APIRouter
from fastapi.param_functions import Depends
from sqlalchemy.orm import Session
from starlette.status import HTTP_201_CREATED

from src.core.database.helpers import master_session, read_session
from src.core.database.models import Item as ItemModel
from src.core.database.models import Order as OrderModel
from src.core.database.models import OrderDetail as OrderDetailModel
from src.core.events import EventCode
from src.core.exceptions import NotFoundError
from src.core.schemas import CreateOrder, GetOrder, Order
from src.core.services.streamer import Streamer, default_streamer

router = APIRouter()


@router.get("/", response_model=List[Order])
async def get_all(query: GetOrder = Depends(), session: Session = Depends(read_session)):
    return OrderModel.get_all(session, query)


@router.get("/{order_id}", response_model=Order)
async def get(order_id: int, session: Session = Depends(read_session)):
    order = OrderModel.get(session, order_id)

    if not order:
        raise NotFoundError(f"Não foi possível localizar a ordem de compra com o ID {order_id}")

    return order


@router.post("/", response_model=Order, status_code=HTTP_201_CREATED)
async def create(
    schema: CreateOrder, session: Session = Depends(master_session), streamer: Streamer = Depends(default_streamer)
):

    for detail in schema.details:
        if not ItemModel.exists(session, item_id=detail.item_id):
            raise NotFoundError(f"Não foi possível localizar o item com o ID {detail.item_id}")

    order = OrderModel.create(session, schema)

    [OrderDetailModel.create(session, detail, order_id=order.id) for detail in schema.details]

    streamer.send_event(event_code=EventCode.CREATE_ORDER, order=order.dict())

    return order
