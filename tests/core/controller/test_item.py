from uuid import uuid4

import pytest
from pydantic import ValidationError
from sqlmodel import Session

from src.core import controller
from src.core.helpers.exceptions import NotFoundError
from src.core.models.context import Context
from src.core.models.item import Item, QueryItem
from tests.factories.item import CreateItemFactory


def test_create_item_success(session: Session, context: Context) -> None:
    # prepare
    schema = CreateItemFactory()
    not_avaliable_schema = CreateItemFactory(amount=0)

    # create
    item = controller.item.create(session, schema, context=context)
    not_avaliable_item = controller.item.create(session, not_avaliable_schema, context=context)

    # assert
    assert item.id is not None
    assert item.code
    assert item.name
    assert item.avaliable

    assert item.code == schema.code
    assert item.name == schema.name
    assert item.cost == schema.cost
    assert item.value == schema.value
    assert item.value > item.cost
    assert not not_avaliable_item.avaliable


def test_create_item_fail(session: Session, context: Context) -> None:
    with pytest.raises(ValidationError):
        CreateItemFactory(code="")

    with pytest.raises(ValidationError):
        CreateItemFactory(name="")

    with pytest.raises(ValidationError):
        CreateItemFactory(value=-1)

    with pytest.raises(ValidationError):
        CreateItemFactory(cost=-1)

    with pytest.raises(ValueError):
        CreateItemFactory(cost=2, value=1)


def test_get_update_item_by_id_success(session: Session, context: Context) -> None:
    # prepare
    schema = CreateItemFactory()

    # create
    item = controller.item.create(session, schema, context=context)
    item2 = controller.item.get_by_id(session, item.id, context=context)

    # assert
    assert item.id == item2.id
    assert item == item2


def test_get_update_item_by_id_fail(session: Session, context: Context) -> None:
    with pytest.raises(NotFoundError):
        controller.item.get_by_id(session, uuid4(), context=context)


def test_get_all_item_success(session: Session, context: Context) -> None:
    query = QueryItem()
    query_avaliable = QueryItem(avaliable=True)
    query_not_avaliable = QueryItem(avaliable=False)

    # create
    for _ in range(5):
        schema = CreateItemFactory()
        controller.item.create(session, schema=schema, context=context)

    for _ in range(5):
        schema = CreateItemFactory(avaliable=False)
        controller.item.create(session, schema=schema, context=context)

    items = controller.item.get_all(session, query_schema=query, context=context)
    items_avaliable = controller.item.get_all(session, query_schema=query_avaliable, context=context)
    items_not_avaliable = controller.item.get_all(session, query_schema=query_not_avaliable, context=context)

    assert all(isinstance(item, Item) for item in items)
    assert all(item.avaliable for item in items_avaliable)
    assert all(not item.avaliable for item in items_not_avaliable)


def test_delete_item_success(session: Session, context: Context) -> None:
    # prepare
    schema = CreateItemFactory()

    # create
    item = controller.item.create(session, schema, context=context)

    deleted_item = controller.item.delete(session, item.id, context=context)

    # assert
    assert item.id == deleted_item.id
    assert item == deleted_item


def test_delete_item_fail(session: Session, context: Context) -> None:
    with pytest.raises(NotFoundError):
        controller.item.delete(session, uuid4(), context=context)
