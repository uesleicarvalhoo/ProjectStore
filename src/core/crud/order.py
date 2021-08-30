from typing import List

import inject
from sqlalchemy.orm import Session

from src.core.database.models import Item as ItemModel
from src.core.database.models import Order as OrderModel
from src.core.database.models import OrderDetail as OrderDetailModel
from src.core.events import EventCode
from src.core.exceptions import NotFoundError
from src.core.schemas import Context, CreateOrder, GetOrder
from src.core.services import Streamer


def get_all(session: Session, query: GetOrder, context: Context) -> List[OrderModel]:
    return OrderModel.get_all(session, query)


def get_by_id(session: Session, order_id: int, context: Context) -> OrderModel:
    return OrderModel.get_by_id(session, order_id)


@inject.params(streamer=Streamer)
def create(session: Session, schema: CreateOrder, context: Context, streamer: Streamer) -> OrderModel:
    for detail in schema.details:
        if not ItemModel.exists(session, item_id=detail.item_id):
            raise NotFoundError(f"Não foi possível salvar a Ordem de compra, item com o ID {detail.item_id} não existe")

    order = OrderModel.create(session, schema)

    [OrderDetailModel.create(session, detail, order_id=order.id) for detail in schema.details]

    streamer.send_event(event_code=EventCode.CREATE_ORDER, context=context, order=order.dict())

    return order


@inject.params(streamer=Streamer)
def delete_by_id(session: Session, order_id: str, context: Context, streamer: Streamer) -> OrderModel:
    order = OrderModel.delete_by_id(session, order_id=order_id)

    if not order:
        raise NotFoundError(f"Não foi possível localizar a ordem de compra com o ID: {order_id}")

    streamer.send_event(EventCode.DELETE_ORDER, context=context, order=order.dict())

    return order
