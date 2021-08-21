from contextlib import suppress

from sqlalchemy.orm import Session

from src.core.database.models import File as FileModel
from src.core.schemas import CreateFile
from tests.utils.faker import random_bucket_key, random_hash


def test_create_file(session: Session):
    # Create Models
    schema = CreateFile(
        bucket_key=random_bucket_key(),
        hash=random_hash(),
    )

    file = FileModel.create(session, schema)

    file2 = FileModel.get(session, file.bucket_key)

    # Assert create
    assert file2 is not None
    assert file.bucket_key == file.bucket_key
    assert file == file

    # Assert schema
    assert file.bucket_key == schema.bucket_key
    assert file.hash == schema.hash


def test_delete_file(session: Session):
    # Create Models
    schema = CreateFile(
        bucket_key=random_bucket_key(),
        hash=random_hash(),
    )

    file = FileModel.create(session, schema)

    file2 = FileModel.delete_by_id(session, file.bucket_key)
    file3 = None

    with suppress(Exception):
        file3 = FileModel.get(session, file.bucket_key)

    # Assert remove
    assert file3 is None

    # Assert models
    assert file.bucket_key == file2.bucket_key
