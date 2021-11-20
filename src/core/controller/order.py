from typing import List
from uuid import UUID

import inject
from sqlmodel import Session, between, select

from src.core.events import EventDescription
from src.core.helpers.exceptions import DataValidationError, NotAuthorizedError, NotFoundError
from src.core.models import (
    Client,
    Context,
    CreateBalance,
    CreateOrder,
    Item,
    Order,
    OrderDetail,
    QueryOrder,
    UpdateOrderStatus,
)
from src.core.services import Streamer

from . import balance


def get_all(session: Session, query_schema: QueryOrder, context: Context) -> List[Order]:
    args = []

    if query_schema.status is not None:
        args.append(Order.status == query_schema.status)

    if not context.user_is_super_user:
        args.append(Order.owner_id == context.user_id)

    if query_schema.start_date is not None and query_schema.end_date is not None:
        args.append(between(Order.date, query_schema.start_date, query_schema.end_date))

    return session.exec(select(Order).where(*args)).all()


def get_by_id(session: Session, order_id: UUID, context: Context) -> Order:
    order = session.exec(select(Order).where(Order.id == order_id)).first()

    if not order:
        raise NotFoundError("Não foi possível localizar a venda com ID: %s" % order_id)

    if not context.user_is_super_user and order.owner_id != context.user_id:
        raise NotAuthorizedError(f"Você não possui permissão para consultar a Venda {order_id}")

    return order


@inject.params(streamer=Streamer)
def register_sale(session: Session, schema: CreateOrder, context: Context, streamer: Streamer) -> Order:
    if not session.exec(select(Client).where(Client.id == schema.client_id)).first():
        raise NotFoundError(f"Não foi possível localizar o cliente com ID: {schema.client_id}")

    checked_ids = []

    for detail in schema.details:
        if detail.item_id in checked_ids:
            continue

        checked_ids.append(detail.item_id)
        item = session.exec(select(Item).where(Item.id == detail.item_id)).first()

        if not item:
            raise NotFoundError(f"Não foi possível salvar a venda, item com o ID {detail.item_id} não existe")

        if item.cost != detail.cost:
            raise DataValidationError(f"O valor de compra do Item {item.name} está incorreto!")

        if detail.sell_value < item.cost:
            raise DataValidationError("O valor de venda de um item não pode ser inferior ao valor de compra!")

        if not item.avaliable:
            raise DataValidationError(f"O item {item.name} de ID {item.id} não está disponível!")

        total_required = sum(x.item_amount for x in schema.details if x.item_id == item.id)

        if item.amount < total_required:
            raise DataValidationError(
                "O item %(name)s não possui estoque suficiente, disponível: %(amount)s, solicitado: %(required)s"
                % {"name": item.name, "amount": item.amount, "required": total_required}
            )

        item.amount -= total_required
        session.add(item)

    order = Order(**schema.dict(exclude={"details": ...}), owner_id=context.user_id)
    session.add(order)

    for detail in schema.details:
        detail_obj = OrderDetail(**detail.dict(), order_id=order.id)
        session.add(detail_obj)

    balance_schema = CreateBalance(
        value=sum(detail.sell_value for detail in schema.details),
        operation=schema.operation.name,
        description=schema.description,
    )
    balance_obj = balance.create(session, balance_schema, context=context)
    session.add(balance_obj)

    session.commit()
    streamer.send_event(description=EventDescription.CREATE_ORDER, context=context, order=order.dict())

    return order


@inject.params(streamer=Streamer)
def delete_by_id(session: Session, order_id: UUID, context: Context, streamer: Streamer) -> Order:
    order = session.exec(select(Order).where(Order.id == order_id)).first()

    if not order:
        raise NotFoundError(f"Não foi possível localizar a venda com o ID: {order_id}")

    if not context.user_is_super_user and order.owner_id != context.user_id:
        raise NotAuthorizedError(f"Você não possui permissão para excluir a Venda {order_id}")

    for detail in [detail for detail in order.details]:
        item = detail.item
        item.amount += detail.item_amount
        session.add(item)

    session.delete(order)
    session.commit()

    streamer.send_event(EventDescription.DELETE_ORDER, context=context, order=order.dict())

    return order


@inject.params(streamer=Streamer)
def update_status(session: Session, schema: UpdateOrderStatus, context: Context, streamer: Streamer) -> None:
    order = session.exec(select(Order).where(Order.id == schema.order_id)).first()

    if not order:
        raise NotFoundError(f"Não foi possível localizar a venda com o ID: {schema.order_id}")

    if not context.user_is_super_user and order.owner_id != context.user_id:
        raise NotAuthorizedError(f"Você não possui permissão para alterar o status da venda {schema.order_id}")

    order.status = schema.status
    session.add(order)
    session.commit()

    streamer.send_event(EventDescription.UPDATE_ORDER, context=context, order=order.dict(), new_status=schema.status)
