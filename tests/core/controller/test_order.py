from uuid import uuid4

import pytest
from pydantic import ValidationError
from sqlmodel import Session

from src.core import controller
from src.core.constants import OrderEnum
from src.core.helpers.exceptions import NotFoundError
from src.core.models.context import Context
from src.core.models.order import UpdateOrderStatus
from tests.factories.client import CreateClientFactory
from tests.factories.fiscal_note import CreateFiscalNoteFactory
from tests.factories.item import CreateItemFactory
from tests.factories.order import CreateOrderFactory
from tests.factories.order_detail import CreateOrderDetailFactory


def test_register_sale_success(session: Session, context: Context) -> None:
    # prepare
    client = controller.client.create(session, CreateClientFactory(), context=context)

    fiscal_note = controller.fiscal_note.create(session, CreateFiscalNoteFactory(), context=context)
    item = controller.item.create(
        session, CreateItemFactory(buy_value=100, sugested_sell_value=150), fiscal_note.id, context=context
    )
    order_detail = CreateOrderDetailFactory(
        item_id=item.id, buy_value=item.buy_value, sell_value=item.sugested_sell_value
    )

    schema = CreateOrderFactory(client_id=client.id, details=[order_detail])

    # create
    order = controller.order.register_sale(session, schema, context=context)

    # assert
    assert order.id is not None
    assert order.client_id == order.client_id
    assert order.status == schema.status
    assert order.description == schema.description
    assert len(order.details) == len(schema.details)
    assert order.profit == 50
    assert order.cost_total == 100
    assert order.sell_total == 150


def test_get_by_id_success(session: Session, context: Context) -> None:
    # prepare
    client = controller.client.create(session, CreateClientFactory(), context=context)

    fiscal_note = controller.fiscal_note.create(session, CreateFiscalNoteFactory(), context=context)
    item = controller.item.create(
        session, CreateItemFactory(buy_value=100, sugested_sell_value=150), fiscal_note.id, context=context
    )
    order_detail = CreateOrderDetailFactory(
        item_id=item.id, buy_value=item.buy_value, sell_value=item.sugested_sell_value
    )

    schema = CreateOrderFactory(client_id=client.id, details=[order_detail])

    # create
    order = controller.order.register_sale(session, schema, context=context)
    order2 = controller.order.get_by_id(session, order.id, context=context)

    assert order.id == order2.id
    assert order == order2


def test_get_by_id_fail(session: Session, context: Context) -> None:
    with pytest.raises(NotFoundError):
        controller.order.get_by_id(session, uuid4(), context=context)


def test_update_order_status_success(session: Session, context: Context) -> None:
    # prepare
    client = controller.client.create(session, CreateClientFactory(), context=context)

    fiscal_note = controller.fiscal_note.create(session, CreateFiscalNoteFactory(), context=context)
    item = controller.item.create(
        session, CreateItemFactory(buy_value=100, sugested_sell_value=150), fiscal_note.id, context=context
    )
    order_detail = CreateOrderDetailFactory(
        item_id=item.id, buy_value=item.buy_value, sell_value=item.sugested_sell_value
    )

    order_schema = CreateOrderFactory(client_id=client.id, details=[order_detail])
    order = controller.order.register_sale(session, order_schema, context=context)
    pending_schema = UpdateOrderStatus(order_id=order.id, status=OrderEnum.PENDING)
    completed_schema = UpdateOrderStatus(order_id=order.id, status=OrderEnum.COMPLETED)
    canceled_schema = UpdateOrderStatus(order_id=order.id, status=OrderEnum.CANCELED)

    # assert Pending
    controller.order.update_status(session, pending_schema, context=context)
    assert order.status == OrderEnum.PENDING

    # assert Completed
    controller.order.update_status(session, completed_schema, context=context)
    assert order.status == OrderEnum.COMPLETED

    # assert Canceled
    controller.order.update_status(session, canceled_schema, context=context)
    assert order.status == OrderEnum.CANCELED


def test_update_order_status_fail(session: Session, context: Context) -> None:
    # prepare
    client = controller.client.create(session, CreateClientFactory(), context=context)

    fiscal_note = controller.fiscal_note.create(session, CreateFiscalNoteFactory(), context=context)
    item = controller.item.create(
        session, CreateItemFactory(buy_value=100, sugested_sell_value=150), fiscal_note.id, context=context
    )
    order_detail = CreateOrderDetailFactory(
        item_id=item.id, buy_value=item.buy_value, sell_value=item.sugested_sell_value
    )

    # create
    order = controller.order.register_sale(
        session, schema=CreateOrderFactory(client_id=client.id, details=[order_detail]), context=context
    )

    # assert
    with pytest.raises(NotFoundError):
        controller.order.update_status(
            session, UpdateOrderStatus(order_id=uuid4(), status=OrderEnum.COMPLETED), context=context
        )

    with pytest.raises(ValidationError):
        controller.order.update_status(session, UpdateOrderStatus(order_id=order.id, status=None), context=context)
