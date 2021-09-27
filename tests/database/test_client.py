from contextlib import suppress

from sqlmodel import Session

from src.core.models import Client as ClientModel
from src.core.models import CreateClient
from tests.utils.faker import random_email, random_name, random_phone


def test_create_client(session: Session):
    # Create Models
    schema = CreateClient(name=random_name(), email=random_email(), phone=random_phone())

    client = ClientModel.create(session, schema)
    client2 = ClientModel.get(session, client.id)

    # Assert Models
    assert client2 is not None
    assert client.id == client2.id
    assert client == client2

    # Assert schema
    assert client.name == schema.name, "Name of client not validated!"
    assert client.email == schema.email, "Email of client not validated!"
    assert client.phone == int(schema.phone), "Phone of client not validated!"


def test_delete_client(session: Session):
    # Create Models
    schema = CreateClient(name=random_name(), email=random_email(), phone=random_phone())

    client = ClientModel.create(session, schema)
    client2 = ClientModel.delete_by_id(session, client.id)
    client3 = None

    with suppress(Exception):
        client3 = ClientModel.get(session, client.id)

    # Assert remove

    assert client3 is None
    assert client.id == client2.id


def test_exists_client(session: Session):
    # Create Models
    schema = CreateClient(name=random_name(), email=random_email(), phone=random_phone())
    client = ClientModel.create(session, schema)

    # Assert exists
    assert ClientModel.exists(session, email=client.email, phone=client.phone)
    assert not ClientModel.exists(session, email="abc")
