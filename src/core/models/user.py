from typing import Any, Dict
from uuid import UUID, uuid4

from pydantic import EmailStr, validator
from sqlmodel import Column, Field, SQLModel

from .base import BaseQuerySchema
from .types import GUID


class BaseUser(SQLModel):
    name: str = Field(..., description="Username")
    email: EmailStr = Field(..., description="Email of the user")
    admin: bool = Field(False, description="Flag to identify super user")

    @validator("name")
    def normalize_name(cls, value: str) -> str:
        if not value:
            raise ValueError("Invalid name")

        if not len(value.split(" ")) > 1:
            raise ValueError("User must be first name and last name.")

        return value.title()


class CreateUser(BaseUser):
    password: str = Field(..., description="User password", min_length=5)
    confirm_password: str = Field(..., description="Password confirmation")

    @validator("confirm_password")
    def validate_password(cls, value: str, values: Dict[str, Any]) -> str:
        if value == values.get("password"):
            return value

        raise ValueError("The password and confirmation must be equal!")


class GetUser(BaseQuerySchema):
    id: UUID = Field(None, description="Identification of User")
    name: str = Field(None, description="Name of user")
    email: EmailStr = Field(None, description="Email of User")


class User(BaseUser, table=True):
    __tablename__ = "users"

    id: UUID = Field(
        default_factory=uuid4, description="ID of the User", sa_column=Column("id", GUID(), primary_key=True)
    )
    password_hash: str = Field(..., description="Hash of password")

    @property
    def is_super_user(self) -> bool:
        return self.admin

    @property
    def first_name(self) -> str:
        return self.name.split(" ")[0]
