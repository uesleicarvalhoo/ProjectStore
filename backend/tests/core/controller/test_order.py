from uuid import uuid4

import pytest
from pydantic import ValidationError
from sqlmodel import Session

from src.core import controller
from src.core.constants import OrderStatus, SaleType
from src.core.helpers.exceptions import DataValidationError, NotFoundError
from src.core.models.context import Context
from src.core.models.order import UpdateOrderStatus
from tests.factories.client import CreateClientFactory
from tests.factories.item import CreateItemFactory
from tests.factories.order import CreateOrderFactory
from tests.factories.order_detail import CreateOrderDetailFactory


def test_register_sale_success(session: Session, context: Context) -> None:
    # prepare
    client = controller.client.create(session, CreateClientFactory(), context=context)

    item = controller.item.create(session, CreateItemFactory(cost=100, value=150), context=context)
    order_detail = CreateOrderDetailFactory(
        item_id=item.id,
        item_name=item.name,
        value=item.value,
        item_amount=item.amount,
    )
    initial_item_amount = item.amount
    schema = CreateOrderFactory(client_id=client.id, items=[order_detail], sale_type=SaleType.SALE_IN_PIX)

    # create
    order = controller.order.register_sale(session, schema, context=context)

    # assert
    assert order.id is not None
    assert order.client_id == order.client_id
    assert order.status == schema.status
    assert order.description == schema.description
    assert len(order.items) == len(schema.items)
    assert item.amount + order.details[0].item_amount == initial_item_amount


def test_register_sale_fail(session: Session, context: Context) -> None:
    # prepare
    client = controller.client.create(session, CreateClientFactory(), context=context)

    item = controller.item.create(session, CreateItemFactory(buy_value=100, sugested_sell_value=150), context=context)

    # Invalid Client
    with pytest.raises(NotFoundError):
        order_detail = CreateOrderDetailFactory(
            item_id=item.id,
            value=item.value,
            item_amount=item.amount,
        )
        controller.order.register_sale(
            session,
            schema=CreateOrderFactory(client_id=uuid4(), items=[order_detail], sale_type=SaleType.SALE_IN_MONEY),
            context=context,
        )

    # Invalid Item
    with pytest.raises(NotFoundError):
        order_detail = CreateOrderDetailFactory(
            item_id=uuid4(),
            value=item.value,
            item_amount=item.amount,
        )
        controller.order.register_sale(
            session,
            schema=CreateOrderFactory(client_id=uuid4(), items=[order_detail], sale_type=SaleType.SALE_IN_CREDIT),
            context=context,
        )

    # Invalid amount
    with pytest.raises(DataValidationError):
        order_detail = CreateOrderDetailFactory(
            item_id=item.id,
            value=item.value,
            item_amount=item.amount + 1,
        )
        controller.order.register_sale(
            session,
            schema=CreateOrderFactory(client_id=client.id, items=[order_detail], sale_type=SaleType.SALE_IN_DEBT),
            context=context,
        )


def test_get_by_id_success(session: Session, context: Context) -> None:
    # prepare
    client = controller.client.create(session, CreateClientFactory(), context=context)

    item = controller.item.create(session, CreateItemFactory(buy_value=100, sugested_sell_value=150), context=context)
    order_detail = CreateOrderDetailFactory(
        item_id=item.id,
        value=item.value,
        item_amount=item.amount,
    )

    schema = CreateOrderFactory(client_id=client.id, items=[order_detail], sale_type=SaleType.SALE_IN_PIX)

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

    item = controller.item.create(session, CreateItemFactory(buy_value=100, sugested_sell_value=150), context=context)
    order_detail = CreateOrderDetailFactory(
        item_id=item.id,
        value=item.value,
        item_amount=item.amount,
    )

    order_schema = CreateOrderFactory(client_id=client.id, items=[order_detail], sale_type=SaleType.SALE_IN_PIX)
    order = controller.order.register_sale(session, order_schema, context=context)
    pending_schema = UpdateOrderStatus(order_id=order.id, status=OrderStatus.PENDING)
    completed_schema = UpdateOrderStatus(order_id=order.id, status=OrderStatus.COMPLETED)
    canceled_schema = UpdateOrderStatus(order_id=order.id, status=OrderStatus.CANCELED)

    # assert Pending
    controller.order.update_status(session, pending_schema, context=context)
    assert order.status == OrderStatus.PENDING

    # assert Completed
    controller.order.update_status(session, completed_schema, context=context)
    assert order.status == OrderStatus.COMPLETED

    # assert Canceled
    controller.order.update_status(session, canceled_schema, context=context)
    assert order.status == OrderStatus.CANCELED


def test_update_order_status_fail(session: Session, context: Context) -> None:
    # prepare
    client = controller.client.create(session, CreateClientFactory(), context=context)

    item = controller.item.create(session, CreateItemFactory(buy_value=100, sugested_sell_value=150), context=context)
    order_detail = CreateOrderDetailFactory(
        item_id=item.id,
        value=item.value,
        item_amount=item.amount,
    )

    # create
    order = controller.order.register_sale(
        session,
        schema=CreateOrderFactory(client_id=client.id, items=[order_detail], sale_type=SaleType.SALE_IN_PIX),
        context=context,
    )

    # assert
    with pytest.raises(NotFoundError):
        controller.order.update_status(
            session, UpdateOrderStatus(order_id=uuid4(), status=OrderStatus.COMPLETED), context=context
        )

    with pytest.raises(ValidationError):
        controller.order.update_status(session, UpdateOrderStatus(order_id=order.id, status=None), context=context)
