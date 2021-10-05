from uuid import uuid4

import pytest
from pydantic import ValidationError
from sqlmodel import Session

from src.core import controller
from src.core.helpers.exceptions import NotFoundError
from src.core.models.context import Context
from src.core.models.item import Item
from tests.factories.fiscal_note import CreateFiscalNoteFactory


def test_create_fiscal_note_success(session: Session, context: Context) -> None:
    # prepare
    schema = CreateFiscalNoteFactory()

    # create
    fiscal_note = controller.fiscal_note.create(session, schema, context=context)

    # assert
    assert fiscal_note.id is not None
    assert fiscal_note.description == schema.description
    assert fiscal_note.purchase_date == schema.purchase_date
    assert len(fiscal_note.items) == len(schema.items)
    assert all(isinstance(item, Item) for item in fiscal_note.items)


def test_create_fiscal_note_fail(session: Session, context: Context) -> None:
    with pytest.raises(ValueError):
        CreateFiscalNoteFactory(image="123")

    with pytest.raises(ValidationError):
        CreateFiscalNoteFactory(filename="")

    with pytest.raises(ValidationError):
        CreateFiscalNoteFactory(description="")


def test_get_fiscal_note_by_id_success(session: Session, context: Context) -> None:
    # prepare
    schema = CreateFiscalNoteFactory()

    # create
    fiscal_note = controller.fiscal_note.create(session, schema, context=context)
    fiscal_note2 = controller.fiscal_note.get_by_id(session, fiscal_note.id, context=context)

    # assert
    assert fiscal_note.id == fiscal_note2.id
    assert fiscal_note == fiscal_note2


def test_get_fiscal_note_by_id_fail(session: Session, context: Context) -> None:
    with pytest.raises(NotFoundError):
        controller.fiscal_note.get_by_id(session, uuid4(), context=context)


def test_delete_fiscal_note_success(session: Session, context: Context) -> None:
    # prepare
    schema = CreateFiscalNoteFactory()

    # create
    fiscal_note = controller.fiscal_note.create(session, schema, context=context)
    deleted_fiscal_note = controller.fiscal_note.delete(session, fiscal_note.id, context=context)

    # assert
    assert fiscal_note.id == deleted_fiscal_note.id
    assert fiscal_note == deleted_fiscal_note

    with pytest.raises(NotFoundError):
        controller.fiscal_note.get_by_id(session, fiscal_note.id, context=context)

    for item in fiscal_note.items:
        with pytest.raises(NotFoundError):
            controller.item.get_by_id(session, item.id, context=context)


def test_delete_fiscal_note_fail(session: Session, context: Context) -> None:
    with pytest.raises(NotFoundError):
        controller.fiscal_note.delete(session, uuid4(), context=context)
