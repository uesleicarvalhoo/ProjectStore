from typing import List
from uuid import UUID

import inject
from sqlmodel import Session, select

from src.core.events import EventCode
from src.core.helpers.exceptions import DataValidationError, NotFoundError
from src.core.models import Client, Context, CreateOrder, GetOrder, Item, Order, OrderDetail, UpdateOrderStatus
from src.core.services import Streamer


def get_all(session: Session, query_schema: GetOrder, context: Context) -> List[Order]:
    query = select(Order).offset(query_schema.offset)

    if query_schema.limit > 0:
        query = query.limit(query_schema.limit)

    return session.exec(query).all()


def get_by_id(session: Session, order_id: UUID, context: Context) -> Order:
    order = session.exec(select(Order).where(Order.id == order_id)).first()

    if not order:
        raise NotFoundError("Não foi possível localizar a venda com ID: %s" % order_id)

    return order


@inject.params(streamer=Streamer)
def register_sale(session: Session, schema: CreateOrder, context: Context, streamer: Streamer) -> Order:
    if not session.exec(select(Client).where(Client.id == schema.client_id)).first():
        raise NotFoundError(f"Não foi possível localizar o cliente com ID: {schema.client_id}")

    for detail in schema.details:
        item = session.exec(select(Item).where(Item.id == detail.item_id)).first()

        if not item:
            raise NotFoundError(f"Não foi possível salvar a venda, item com o ID {detail.item_id} não existe")

        if item.buy_value != detail.buy_value:
            raise DataValidationError(f"O valor de compra do Item {item.name} está incorreto!")

        if detail.sell_value < item.buy_value:
            raise DataValidationError("O valor de venda de um item não pode ser inferior ao valor de compra!")

        if not item.avaliable:
            raise DataValidationError(f"O item {item.name} de ID {item.id} não está disponível!")

    order = Order(**schema.dict(exclude={"details": ...}))
    session.add(order)

    for detail in schema.details:
        detail_obj = OrderDetail(**detail.dict(), order_id=order.id)
        session.add(detail_obj)

    for item in [order.item for order in order.details]:
        item.avaliable = False
        session.add(item)

    session.commit()

    streamer.send_event(event_code=EventCode.CREATE_ORDER, context=context, order=order.dict())

    return order


@inject.params(streamer=Streamer)
def delete_by_id(session: Session, order_id: UUID, context: Context, streamer: Streamer) -> Order:
    order = session.exec(select(Order).where(Order.id == order_id)).first()

    if not order:
        raise NotFoundError(f"Não foi possível localizar a venda com o ID: {order_id}")

    for item in [order.item for order in order.details]:
        item.avaliable = True
        session.add(item)

    session.delete(order)
    session.commit()

    streamer.send_event(EventCode.DELETE_ORDER, context=context, order=order.dict())

    return order


@inject.params(streamer=Streamer)
def update_status(session: Session, schema: UpdateOrderStatus, context: Context, streamer: Streamer) -> None:
    order = session.exec(select(Order).where(Order.id == schema.order_id)).first()

    if not order:
        raise NotFoundError(f"Não foi possível localizar a venda com o ID: {schema.order_id}")

    order.status = schema.status
    session.add(order)
    session.commit()

    streamer.send_event(EventCode.UPDATE_ORDER, context=context, order=order.dict(), new_status=schema.status)
