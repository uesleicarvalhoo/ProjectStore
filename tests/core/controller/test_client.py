import re
from uuid import uuid4

import pytest
from pydantic import ValidationError
from sqlmodel import Session

from src.core import controller
from src.core.helpers.exceptions import NotFoundError
from src.core.models.client import Client, CreateClient, QueryClient, UpdateClient
from src.core.models.context import Context
from tests.factories.client import CreateClientFactory


def test_create_client(session: Session, context: Context):
    # prepare
    schema = CreateClientFactory()

    # create
    client = controller.client.create(session, schema, context=context)

    # assert
    assert client.id is not None
    assert client.name == schema.name
    assert client.email == schema.email
    assert client.phone == schema.phone

    assert re.match(r"[^@]+@[^@]+\.[^@]+", client.email) is not None


def test_create_client_fail(session: Session, context: Context) -> None:
    with pytest.raises(ValidationError):
        controller.client.create(session, schema=CreateClient(), context=Context)

    with pytest.raises(ValidationError):
        controller.client.create(session, schema=CreateClientFactory(name=""), context=Context)

    with pytest.raises(ValidationError):
        controller.client.create(session, schema=CreateClientFactory(phone=""), context=Context)

    with pytest.raises(ValidationError):
        controller.client.create(session, schema=CreateClientFactory(email=""), context=Context)


def test_get_all_success(session: Session, context: Context) -> None:
    # prepare
    query = QueryClient(limit=10, page=1)
    query2 = QueryClient(limit=5, page=2)

    # create
    for _ in range(10):
        schema = CreateClientFactory()
        controller.client.create(session, schema=schema, context=context)

    clients = controller.client.get_all(session, query_schema=query, context=context)
    clients2 = controller.client.get_all(session, query_schema=query2, context=context)

    # assert
    assert query.offset == 0
    assert query2.offset == 5

    assert isinstance(clients, list)
    assert len(clients) == query.limit
    assert all(isinstance(client, Client) for client in clients)
    assert len(clients2) == query2.limit


def test_get_by_id_success(session: Session, context: Context) -> None:
    # prepare
    schema = CreateClientFactory()

    # create
    client = controller.client.create(session, schema, context=context)

    client2 = controller.client.get_by_id(session, client.id, context=context)

    assert client.id == client2.id
    assert client.name == client2.name
    assert client.email == client2.email
    assert client.phone == client2.phone
    assert client2 == client


def test_get_by_id_fail(session: Session, context: Context) -> None:
    with pytest.raises(NotFoundError):
        controller.client.get_by_id(session, uuid4(), context=context)


def test_delete_success(session: Session, context: Context) -> None:
    # prepare
    schema = CreateClientFactory()

    # create
    client = controller.client.create(session, schema, context=context)
    deleted_client = controller.client.delete(session, client.id, context=Context)

    # assert
    assert client.id == deleted_client.id
    assert client == deleted_client

    with pytest.raises(NotFoundError):
        controller.client.get_by_id(session, client.id, context=Context)


def test_delete_fail(session: Session, context: Context) -> None:
    with pytest.raises(NotFoundError):
        controller.client.delete(session, uuid4(), context=context)


def test_update_success(session: Session, context: Context) -> None:
    # prepare
    schema = CreateClientFactory()
    client = controller.client.create(session, schema, context=context)

    update_schema = UpdateClient(id=client.id, name="New client name", email="newemail@example.com", phone=12987654321)

    # create
    controller.client.update(session, update_schema, context=context)

    assert client.name.lower() == update_schema.name.lower()
    assert client.email == update_schema.email
    assert client.phone == update_schema.phone
