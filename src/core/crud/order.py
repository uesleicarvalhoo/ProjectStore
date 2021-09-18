from typing import List

import inject
from sqlalchemy.orm import Session

from src.core.database.models import Item as ItemModel
from src.core.database.models import Order as OrderModel
from src.core.database.models import OrderDetail as OrderDetailModel
from src.core.events import EventCode
from src.core.exceptions import NotFoundError, ValidationError
from src.core.schemas import Context, CreateOrder, GetOrder
from src.core.schemas.order import UpdateOrderStatus
from src.core.services import Streamer


def get_all(session: Session, query: GetOrder, context: Context) -> List[OrderModel]:
    return OrderModel.get_all(session, query)


def get_by_id(session: Session, order_id: int, context: Context) -> OrderModel:
    order = OrderModel.get_by_id(session, order_id)

    if not order:
        raise NotFoundError("Não foi possível localizar a venda com ID: %s" % order_id)

    return order


@inject.params(streamer=Streamer)
def create(session: Session, schema: CreateOrder, context: Context, streamer: Streamer) -> OrderModel:
    for detail in schema.details:
        item = ItemModel.get(session, item_id=detail.item_id)

        if not item:
            raise NotFoundError(f"Não foi possível salvar a venda, item com o ID {detail.item_id} não existe")

        if item.buy_value != detail.buy_value:
            raise ValidationError(f"O valor de compra do Item {item.name} está incorreto!")

        if detail.sell_value < item.buy_value:
            raise ValidationError("O valor de venda de um item não pode ser inferior ao valor de compra!")

    order = OrderModel.create(session, schema)

    [OrderDetailModel.create(session, detail, order_id=order.id) for detail in schema.details]

    streamer.send_event(event_code=EventCode.CREATE_ORDER, context=context, order=order.dict())

    return order


@inject.params(streamer=Streamer)
def delete_by_id(session: Session, order_id: str, context: Context, streamer: Streamer) -> OrderModel:
    order = OrderModel.delete_by_id(session, order_id=order_id)

    if not order:
        raise NotFoundError(f"Não foi possível localizar a venda com o ID: {order_id}")

    streamer.send_event(EventCode.DELETE_ORDER, context=context, order=order.dict())

    return order


@inject.params(streamer=Streamer)
def update_status(session: Session, schema: UpdateOrderStatus, context: Context, streamer: Streamer):
    order = OrderModel.get(session, schema.order_id)

    if not order:
        raise NotFoundError(f"Não foi possível localizar a venda com o ID: {schema.id}")

    streamer.send_event(EventCode.UPDATE_ORDER, context=context, order=order.dict(), new_status=schema.status)

    order.update(session, {"status": schema.status}, auto_commit=True)
