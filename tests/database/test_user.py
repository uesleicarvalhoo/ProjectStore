import random

from sqlmodel import Session

from src.core.models import CreateUser
from src.core.models import User as UserModel
from src.core.security import verify_password
from tests.utils.faker import random_email, random_name, random_password


def test_create_user(session: Session):
    password = random_password()
    schema = CreateUser(
        name=random_name(),
        email=random_email(),
        password=password,
        confirm_password=password,
        admin=random.choice([True, False]),
    )

    user = UserModel.create(session, schema)
    user2 = UserModel.get(session, user.id)

    assert user2.id == user.id
    assert user2.id is not None
    assert user.name == schema.name
    assert user.email == schema.email
    assert user.admin == schema.admin
    assert verify_password(schema.password, user.password_hash)
