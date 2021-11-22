import pytest

from src.core.constants import AccessLevel
from src.core.models.user import User
from src.core.security import (
    create_access_token,
    generate_password_reset_token,
    get_password_hash,
    load_jwt_token,
    verify_password,
    verify_password_reset_token,
)


def test_test_create_acess_token_success(current_user: User):
    sub = str(current_user.id)
    encoded_token, _ = create_access_token(sub, access_level=current_user.access_level)
    token = load_jwt_token(encoded_token)

    assert str(token.sub) == sub


def test_create_access_token_fail():
    with pytest.raises(ValueError):
        create_access_token("", access_level=AccessLevel.USER)


def test_verify_password_success():
    password = "secret123"
    password_hash = get_password_hash(password)

    assert password != password_hash
    assert verify_password(password, password_hash)


def test_verify_password_fail():
    password = "fail123"
    invalid_hash = get_password_hash("invalid")

    assert not verify_password(password, invalid_hash)


def test_generate_password_reset_token_success():
    email = "ueser@email.com"

    password_reset_token = generate_password_reset_token(email)
    verified_email = verify_password_reset_token(password_reset_token)

    assert password_reset_token != email
    assert verified_email == email


def test_generate_password_reset_token_fail():
    fake_token = "iamafaketoken!"
    verified_email = verify_password_reset_token(fake_token)

    assert verified_email is None
