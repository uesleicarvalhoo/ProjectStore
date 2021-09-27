from base64 import b64encode
from contextlib import suppress

from sqlmodel import Session

from src.core.models import CreateFile, CreateFiscalNote
from src.core.models import File as FileModel
from src.core.models import FiscalNote as FiscalNoteModel
from tests.utils.faker import random_bucket_key, random_date, random_description, random_filename, random_hash


def test_create_fical_note(session: Session):
    # Create Models
    file = FileModel.create(
        session,
        CreateFile(
            bucket_key=random_bucket_key(),
            hash=random_hash(),
        ),
    )

    # Create FiscalNote
    with open("tests/static/fiscal_note.png", "rb") as f:
        fn = b64encode(f.read())

    schema = CreateFiscalNote(
        description=random_description(),
        purchase_date=random_date(),
        file_id=file.bucket_key,
        filename=random_filename("image", "png"),
        image=fn,
    )

    fiscal_note = FiscalNoteModel.create(session, schema, file=file)
    fiscal_note2 = FiscalNoteModel.get(session, fiscal_note.id)

    # Assert create
    assert fiscal_note2 is not None, "Fiscal note not created!"
    assert fiscal_note.id == fiscal_note2.id
    assert fiscal_note == fiscal_note2

    # Assert schema
    assert fiscal_note.description == schema.description
    assert fiscal_note.purchase_date == schema.purchase_date
    assert fiscal_note.file_id == schema.file_id

    # Assert relationship
    assert fiscal_note.file_id == fiscal_note.file.bucket_key


def test_delete_fiscal_note(session: Session):
    # Create Models
    file = FileModel.create(
        session,
        CreateFile(
            bucket_key=random_bucket_key(),
            hash=random_hash(),
        ),
    )

    # Create FiscalNote
    with open("tests/static/fiscal_note.png", "rb") as f:
        fn = b64encode(f.read())

    schema = CreateFiscalNote(
        description=random_description(),
        purchase_date=random_date(),
        file_id=file.bucket_key,
        filename=random_filename("image", "png"),
        image=fn,
    )

    fiscal_note = FiscalNoteModel.create(session, schema, file)
    fiscal_note2 = FiscalNoteModel.delete_by_id(session, fiscal_note.id)
    fiscal_note3 = None

    with suppress(Exception):
        fiscal_note3 = FiscalNoteModel.get(session, fiscal_note.id)

    # Assert remove
    assert fiscal_note3 is None

    # Assert models
    assert fiscal_note.id == fiscal_note2.id
