from sqlmodel import Session

from src.core import controller
from src.core.models import Context
from tests.factories.file import CreateFileFactory


def test_get_or_create_file(session: Session, context: Context):
    schema = CreateFileFactory()

    file = controller.file.get_or_create_file(session, "test", schema.filename, schema.data, context=context)

    assert file.bucket_key is not None
    assert file.bucket_key is not ...
