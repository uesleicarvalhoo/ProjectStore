from uuid import uuid4

import pytest

from src.core.security import (
    create_access_token,
    get_password_hash,
    load_jwt_token,
    validate_access_token,
    verify_password,
)


def test_test_create_acess_token_success():
    sub = str(uuid4())
    encoded_token = create_access_token(sub)
    token = load_jwt_token(encoded_token)

    assert encoded_token is not None
    assert str(token.sub) == sub
    assert validate_access_token(encoded_token)


def test_create_access_token_fail():
    with pytest.raises(ValueError):
        create_access_token("")


def test_validate_access_token_success():
    token = create_access_token(str(uuid4()))
    assert validate_access_token(token)


def test_validate_access_token_fail():
    token = create_access_token(str(uuid4()), expires_delta=-1)
    assert not validate_access_token(token)


def test_verify_password_success():
    password = "secret123"
    password_hash = get_password_hash(password)

    assert password != password_hash
    assert verify_password(password, password_hash)


def test_verify_password_fail():
    password = "fail123"
    invalid_hash = get_password_hash("invalid")

    assert not verify_password(password, invalid_hash)
