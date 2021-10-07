from typing import TYPE_CHECKING, Any, Dict, List
from uuid import UUID, uuid4

from pydantic import EmailStr, validator
from sqlmodel import Column, Enum, Field, Relationship, SQLModel
from sqlmodel.sql.sqltypes import GUID

from src.core.constants import AccessLevel

from .base import BaseQuerySchema

if TYPE_CHECKING:
    from .client import Client
    from .fiscal_note import FiscalNote
    from .item import Item
    from .order import Order


class BaseUser(SQLModel):
    name: str = Field(..., description="Username")
    email: EmailStr = Field(..., description="Email of the user")
    access_level: AccessLevel = Field(
        AccessLevel.USER,
        description="Level of access access permission of that user",
        sa_column=Column(Enum(AccessLevel), nullable=False),
    )
    active: bool = Field(True, description="Flag to identify if user is active")

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


class QueryUser(BaseQuerySchema):
    pass


class User(BaseUser, table=True):
    __tablename__ = "users"

    id: UUID = Field(
        default_factory=uuid4, description="ID of the User", sa_column=Column("id", GUID(), primary_key=True)
    )
    password_hash: str = Field(..., description="Hash of password")

    items: List["Item"] = Relationship(
        back_populates="owner",
        sa_relationship_kwargs={"cascade": "all,delete", "lazy": "selectin", "passive_deletes": True},
    )

    fiscal_notes: List["FiscalNote"] = Relationship(
        back_populates="owner",
        sa_relationship_kwargs={"cascade": "all,delete", "lazy": "selectin", "passive_deletes": True},
    )

    clients: List["Client"] = Relationship(
        back_populates="owner",
        sa_relationship_kwargs={"cascade": "all,delete", "lazy": "selectin", "passive_deletes": True},
    )

    orders: List["Order"] = Relationship(
        back_populates="owner",
        sa_relationship_kwargs={"cascade": "all,delete", "lazy": "selectin", "passive_deletes": True},
    )

    @property
    def is_super_user(self) -> bool:
        return self.access_level == AccessLevel.SUPER_USER

    @property
    def is_active(self) -> bool:
        return self.active

    @property
    def first_name(self) -> str:
        return self.name.split(" ")[0]
