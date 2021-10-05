from uuid import uuid4

import pytest
from pydantic import ValidationError
from sqlmodel import Session

from src.core import controller
from src.core.helpers.exceptions import NotFoundError
from src.core.models.context import Context
from src.core.models.item import Item, QueryItem
from tests.factories.fiscal_note import CreateFiscalNoteFactory
from tests.factories.item import CreateItemFactory


def test_create_item_success(session: Session, context: Context) -> None:
    # prepare
    fiscal_note_schema = CreateFiscalNoteFactory(items=[])
    schema = CreateItemFactory()
    not_avaliable_schema = CreateItemFactory(avaliable=False)

    # create
    fiscal_note = controller.fiscal_note.create(session, fiscal_note_schema, context=context)
    item = controller.item.create(session, schema, fiscal_note.id, context=context)
    not_avaliable_item = controller.item.create(session, not_avaliable_schema, fiscal_note.id, context=context)

    # assert
    assert item.id is not None
    assert item.code
    assert item.name
    assert item.avaliable

    assert item.code == schema.code
    assert item.name == schema.name
    assert item.buy_value == schema.buy_value
    assert item.sugested_sell_value == schema.sugested_sell_value
    assert item.sugested_sell_value > item.buy_value
    assert not not_avaliable_item.avaliable


def test_create_item_fail(session: Session, context: Context) -> None:
    with pytest.raises(ValidationError):
        CreateItemFactory(code="")

    with pytest.raises(ValidationError):
        CreateItemFactory(name="")

    with pytest.raises(ValidationError):
        CreateItemFactory(buy_value=-1)

    with pytest.raises(ValidationError):
        CreateItemFactory(sugested_sell_value=-1)

    with pytest.raises(ValueError):
        CreateItemFactory(buy_value=2, sugested_sell_value=1)


def test_get_item_by_id_success(session: Session, context: Context) -> None:
    # prepare
    fiscal_note_schema = CreateFiscalNoteFactory(items=[])
    schema = CreateItemFactory()

    # create
    fiscal_note = controller.fiscal_note.create(session, fiscal_note_schema, context=context)
    item = controller.item.create(session, schema, fiscal_note.id, context=context)
    item2 = controller.item.get_by_id(session, item.id, context=context)

    # assert
    assert item.id == item2.id
    assert item == item2


def test_get_item_by_id_fail(session: Session, context: Context) -> None:
    with pytest.raises(NotFoundError):
        controller.item.get_by_id(session, uuid4(), context=context)


def test_get_all_item_success(session: Session, context: Context) -> None:
    query = QueryItem(limit=10, page=1)
    query2 = QueryItem(limit=5, page=2)
    query_avaliable = QueryItem(avaliable=True)
    query_not_avaliable = QueryItem(avaliable=False)

    # create
    fiscal_note = controller.fiscal_note.create(session, CreateFiscalNoteFactory(), context=context)
    for _ in range(5):
        schema = CreateItemFactory()
        controller.item.create(session, schema=schema, fiscal_note_id=fiscal_note.id, context=context)

    for _ in range(5):
        schema = CreateItemFactory(avaliable=False)
        controller.item.create(session, schema=schema, fiscal_note_id=fiscal_note.id, context=context)

    items = controller.item.get_all(session, query_schema=query, context=context)
    items2 = controller.item.get_all(session, query_schema=query2, context=context)
    items_avaliable = controller.item.get_all(session, query_schema=query_avaliable, context=context)
    items_not_avaliable = controller.item.get_all(session, query_schema=query_not_avaliable, context=context)

    assert query.offset == 0
    assert query2.offset == 5
    assert query.limit == 10
    assert query2.limit == 5

    assert all(isinstance(item, Item) for item in items)
    assert len(items) == 10
    assert len(items2) == 5
    assert all(item.avaliable for item in items_avaliable)
    assert all(not item.avaliable for item in items_not_avaliable)


def test_delete_item_success(session: Session, context: Context) -> None:
    # prepare
    fiscal_note_schema = CreateFiscalNoteFactory(items=[])
    schema = CreateItemFactory()

    # create
    fiscal_note = controller.fiscal_note.create(session, fiscal_note_schema, context=context)
    item = controller.item.create(session, schema, fiscal_note.id, context=context)

    deleted_item = controller.item.delete(session, item.id, context=context)
    fiscal_note2 = controller.fiscal_note.get_by_id(session, fiscal_note.id, context=context)

    # assert
    assert item.id == deleted_item.id
    assert item == deleted_item
    assert fiscal_note2 is not None
    assert fiscal_note == fiscal_note2


def test_delete_item_fail(session: Session, context: Context) -> None:
    with pytest.raises(NotFoundError):
        controller.item.delete(session, uuid4(), context=context)
