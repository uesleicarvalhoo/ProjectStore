from uuid import uuid4

import pytest
from pydantic import ValidationError
from sqlmodel import Session

from src.core import controller
from src.core.helpers.exceptions import NotFoundError
from src.core.models.context import Context
from src.core.models.fiscal_note_item import FiscalNoteItem, QueryFiscalNoteItem
from tests.factories.fiscal_note import CreateFiscalNoteFactory
from tests.factories.fiscal_note_item import CreateFiscalNoteItemFactory


def test_create_fiscal_note_item_success(session: Session, context: Context) -> None:
    # prepare
    fiscal_note_schema = CreateFiscalNoteFactory(items=[])
    schema = CreateFiscalNoteItemFactory()

    # create
    fiscal_note = controller.fiscal_note.create(session, fiscal_note_schema, context=context)
    fiscal_note_item = controller.fiscal_note_item.create(session, schema, fiscal_note.id, context=context)

    # assert

    assert fiscal_note_item.id is not None
    assert fiscal_note_item.code
    assert fiscal_note_item.name

    assert fiscal_note_item.code == schema.code
    assert fiscal_note_item.name == schema.name
    assert fiscal_note_item.buy_value == schema.buy_value
    assert fiscal_note_item.sugested_sell_value == schema.sugested_sell_value
    assert fiscal_note_item.sugested_sell_value > fiscal_note_item.buy_value


def test_create_fiscal_note_item_fail(session: Session, context: Context) -> None:
    with pytest.raises(ValidationError):
        CreateFiscalNoteItemFactory(code="")

    with pytest.raises(ValidationError):
        CreateFiscalNoteItemFactory(name="")

    with pytest.raises(ValidationError):
        CreateFiscalNoteItemFactory(buy_value=-1)

    with pytest.raises(ValidationError):
        CreateFiscalNoteItemFactory(sugested_sell_value=-1)

    with pytest.raises(ValueError):
        CreateFiscalNoteItemFactory(buy_value=2, sugested_sell_value=1)


def test_get_fiscal_note_update_item_by_id_success(session: Session, context: Context) -> None:
    # prepare
    fiscal_note_schema = CreateFiscalNoteFactory(items=[])
    schema = CreateFiscalNoteItemFactory()

    # create
    fiscal_note = controller.fiscal_note.create(session, fiscal_note_schema, context=context)
    fiscal_note_item = controller.fiscal_note_item.create(session, schema, fiscal_note.id, context=context)
    fiscal_note_item2 = controller.fiscal_note_item.get_by_id(session, fiscal_note_item.id, context=context)

    # assert
    assert fiscal_note_item.id == fiscal_note_item2.id
    assert fiscal_note_item == fiscal_note_item2


def test_get_fiscal_note_update_item_by_id_fail(session: Session, context: Context) -> None:
    with pytest.raises(NotFoundError):
        controller.fiscal_note_item.get_by_id(session, uuid4(), context=context)


def test_get_all_fiscal_note_item_success(session: Session, context: Context) -> None:
    query = QueryFiscalNoteItem(limit=10, page=1)
    query2 = QueryFiscalNoteItem(limit=5, page=2)

    # create
    fiscal_note = controller.fiscal_note.create(session, CreateFiscalNoteFactory(items=[]), context=context)

    for _ in range(5):
        schema = CreateFiscalNoteItemFactory()
        controller.fiscal_note_item.create(session, schema=schema, fiscal_note_id=fiscal_note.id, context=context)

    for _ in range(5):
        schema = CreateFiscalNoteItemFactory(avaliable=False)
        controller.fiscal_note_item.create(session, schema=schema, fiscal_note_id=fiscal_note.id, context=context)

    items = controller.fiscal_note_item.get_all(session, query_schema=query, context=context)
    fiscal_note_item2 = controller.fiscal_note_item.get_all(session, query_schema=query2, context=context)

    assert query.offset == 0
    assert query2.offset == 5
    assert query.limit == 10
    assert query2.limit == 5

    assert all(isinstance(item, FiscalNoteItem) for item in items)
    assert len(items) == 10
    assert len(fiscal_note_item2) == 5


def test_delete_fiscal_note_item_success(session: Session, context: Context) -> None:
    # prepare
    fiscal_note_schema = CreateFiscalNoteFactory(items=[])
    schema = CreateFiscalNoteItemFactory()

    # create
    fiscal_note = controller.fiscal_note.create(session, fiscal_note_schema, context=context)
    item = controller.fiscal_note_item.create(session, schema, fiscal_note.id, context=context)

    deleted_item = controller.fiscal_note_item.delete(session, item.id, context=context)
    fiscal_note2 = controller.fiscal_note.get_by_id(session, fiscal_note.id, context=context)

    # assert
    assert item.id == deleted_item.id
    assert item == deleted_item
    assert fiscal_note2 is not None
    assert fiscal_note == fiscal_note2


def test_delete_fiscal_note_item_fail(session: Session, context: Context) -> None:
    with pytest.raises(NotFoundError):
        controller.fiscal_note_item.delete(session, uuid4(), context=context)
