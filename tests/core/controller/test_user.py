import re
from uuid import uuid4

import pytest
from pydantic import ValidationError
from sqlmodel import Session

from src.core import controller
from src.core.config import settings
from src.core.constants import AccessLevel
from src.core.helpers.exceptions import NotFoundError
from src.core.models.context import Context
from src.core.models.user import CreateUser, QueryUser, User
from src.core.security import verify_password
from tests.factories.user import CreateUserFactory


def test_create_user_success(session: Session, context: Context) -> None:
    # prepare
    schema = CreateUserFactory(admin=False)
    admin_schema = CreateUserFactory(access_level=AccessLevel.SUPER_USER)

    # create
    user = controller.user.create(session, schema, context=context)
    user_admin = controller.user.create(session, admin_schema, context=context)

    # assert
    assert user.id is not None
    assert user.name == schema.name
    assert user.email == schema.email
    assert user.access_level == schema.access_level
    assert not user.is_super_user

    assert user_admin.id is not None
    assert user_admin.name == admin_schema.name
    assert user_admin.email == admin_schema.email
    assert user_admin.access_level == admin_schema.access_level
    assert user_admin.is_super_user

    assert len(user.first_name.split(" ")) == 1
    assert len(user_admin.first_name.split(" ")) == 1

    assert re.match(r"[^@]+@[^@]+\.[^@]+", user.email) is not None
    assert re.match(r"[^@]+@[^@]+\.[^@]+", user_admin.email) is not None


def test_create_user_fail(session: Session, context: Context) -> None:
    with pytest.raises(ValidationError):
        controller.user.create(session, schema=CreateUser(), context=Context)

    with pytest.raises(ValidationError):
        controller.user.create(session, schema=CreateUserFactory(name=""), context=Context)

    with pytest.raises(ValidationError):
        controller.user.create(session, schema=CreateUserFactory(access_level=None), context=Context)

    with pytest.raises(ValidationError):
        controller.user.create(session, schema=CreateUserFactory(email=""), context=Context)

    with pytest.raises(ValidationError):
        controller.user.create(session, schema=CreateUserFactory(password=""), context=Context)

    with pytest.raises(ValidationError):
        controller.user.create(
            session, schema=CreateUserFactory(password="123456", confirm_password="654321"), context=Context
        )


def test_get_by_id_success(session: Session, context: Context) -> None:
    # prepare
    schema = CreateUserFactory()

    # create
    user = controller.user.create(session, schema, context=context)

    user2 = controller.user.get_by_id(session, user.id, context=context)

    assert user.id == user2.id
    assert user.name == user2.name
    assert user.email == user2.email
    assert user.is_super_user == user2.is_super_user
    assert user.password_hash == user2.password_hash
    assert user == user2


def test_get_by_id_fail(session: Session, context: Context) -> None:
    with pytest.raises(NotFoundError):
        controller.user.get_by_id(session, uuid4(), context=context)


def test_validate_create_of_first_super_user(session: Session, context: Context) -> None:
    user = controller.user.get_by_email(session, settings.FIRST_SUPERUSER_EMAIL, context=context)

    assert user.email == settings.FIRST_SUPERUSER_EMAIL
    assert user.is_super_user
    assert user.name == settings.FIRST_SUPERUSER_NAME
    assert verify_password(settings.FIRST_SUPERUSER_PASSWORD, user.password_hash)


def test_get_by_email_success(session: Session, context: Context) -> None:
    # prepare
    schema = CreateUserFactory()

    # create
    user = controller.user.create(session, schema, context=context)

    user2 = controller.user.get_by_email(session, user.email, context=context)

    assert user.id == user2.id
    assert user.name == user2.name
    assert user.email == user2.email
    assert user.access_level == user2.access_level
    assert user.password_hash == user2.password_hash
    assert user.is_super_user == user2.is_super_user
    assert user == user2


def test_get_by_email_fail(session: Session, context: Context) -> None:
    with pytest.raises(NotFoundError):
        controller.user.get_by_email(session, "randomemail@random.com", context=context)


def test_get_all_success(session: Session, context: Context) -> None:
    # prepare
    query = QueryUser(limit=10, page=1)
    query2 = QueryUser(limit=5, page=2)

    # create
    for _ in range(10):
        schema = CreateUserFactory()
        controller.user.create(session, schema=schema, context=context)

    users = controller.user.get_all(session, query_schema=query, context=context)
    users2 = controller.user.get_all(session, query_schema=query2, context=context)

    # assert
    assert query.offset == 0
    assert query2.offset == 5
    assert query.limit == 10
    assert query2.limit == 5

    assert isinstance(users, list)
    assert len(users) == query.limit
    assert all(isinstance(user, User) for user in users)
    assert len(users2) == query2.limit


def test_delete_success(session: Session, context: Context) -> None:
    # prepare
    schema = CreateUserFactory()

    # create
    user = controller.user.create(session, schema, context=context)
    deleted_user = controller.user.delete(session, user.id, context=Context)

    # assert
    assert user.id == deleted_user.id
    assert user == deleted_user

    with pytest.raises(NotFoundError):
        controller.user.get_by_id(session, user.id, context=Context)


def test_delete_fail(session: Session, context: Context) -> None:
    with pytest.raises(NotFoundError):
        controller.user.delete(session, uuid4(), context=context)


def test_authenticate_success(session: Session, context: Context) -> None:
    schema = CreateUserFactory()
    user = controller.user.create(session, schema, context=context)

    assert verify_password(schema.password, user.password_hash)


def test_authenticate_fail(session: Session, context: Context) -> None:
    schema = CreateUserFactory()
    user = controller.user.create(session, schema, context=context)

    assert not verify_password("123456", user.password_hash)
