from base64 import b64encode
from contextlib import suppress
from random import choice

from sqlalchemy.orm import Session

from src.core.database.models import File as FileModel
from src.core.database.models import FiscalNote as FiscalNoteModel
from src.core.database.models import Item as ItemModel
from src.core.schemas import CreateFile, CreateFiscalNote, CreateItem
from tests.utils import faker


def test_create_item(session: Session):
    # Create FiscalNote
    with open("tests/static/fiscal_note.png", "rb") as f:
        fn_image = b64encode(f.read())

    fn_file = FileModel.create(
        session,
        CreateFile(
            bucket_key=faker.random_bucket_key(),
            hash=faker.random_hash(),
        ),
    )

    fiscal_note = FiscalNoteModel.create(
        session,
        CreateFiscalNote(
            description=faker.random_description(),
            purchase_date=faker.random_date(),
            file_id=fn_file.bucket_key,
            filename=faker.random_filename("image", "png"),
            image=fn_image,
        ),
        fn_file,
    )

    # Create Item
    with open("tests/static/fiscal_note.png", "rb") as f:
        item_image = b64encode(f.read())

    file = FileModel.create(session, CreateFile(bucket_key=faker.random_bucket_key(), hash=faker.random_hash()))

    schema = CreateItem(
        code=faker.random_lower_string(),
        avaliable=choice([True, False]),
        buy_value=faker.random_float_value(),
        fiscal_note_id=fiscal_note.id,
        filename=faker.random_filename("image", "png"),
        image=item_image,
    )

    item = ItemModel.create(session, schema, fiscal_note.id, file)

    item2 = ItemModel.get(session, item.id)

    # Assert creation
    assert item2 is not None
    assert item.id == item2.id
    assert item == item2

    # Assert Schema
    assert item.code == schema.code
    assert item.avaliable == schema.avaliable
    assert item.buy_value == schema.buy_value

    # Assert relationship
    assert item.file_id == item.file.bucket_key
    assert item.fiscal_note_id == item.fiscal_note.id


def test_delete_item(session: Session):
    # Create FiscalNote
    with open("tests/static/fiscal_note.png", "rb") as f:
        fn_image = b64encode(f.read())

    fn_item = FileModel.create(
        session,
        CreateFile(
            bucket_key=faker.random_bucket_key(),
            hash=faker.random_hash(),
        ),
    )

    fiscal_note = FiscalNoteModel.create(
        session,
        CreateFiscalNote(
            description=faker.random_description(),
            purchase_date=faker.random_date(),
            file_id=fn_item.bucket_key,
            filename=faker.random_filename("image", "png"),
            image=fn_image,
        ),
        fn_item,
    )

    # Create Item
    with open("tests/static/fiscal_note.png", "rb") as f:
        item_image = b64encode(f.read())

    file = FileModel.create(session, CreateFile(bucket_key=faker.random_bucket_key(), hash=faker.random_hash()))

    schema = CreateItem(
        code=faker.random_lower_string(),
        avaliable=choice([True, False]),
        buy_value=faker.random_float_value(),
        filename=faker.random_filename("image", "png"),
        image=item_image,
    )

    item = ItemModel.create(session, schema, fiscal_note.id, file)
    item2 = ItemModel.get(session, item.id)

    # Query
    item = ItemModel.create(session, schema, fiscal_note.id, file)
    item2 = ItemModel.delete_by_id(session, item.id)
    item3 = None

    # Assert remove
    with suppress(Exception):
        item3 = ItemModel.get(session, item.id)

    assert item3 is None

    # Assert model
    assert item.id == item2.id
