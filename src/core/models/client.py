from datetime import datetime
from typing import TYPE_CHECKING, List
from uuid import UUID, uuid4

from pydantic import EmailStr, constr, validator
from sqlmodel import Column, Field, Relationship, SQLModel
from sqlmodel.sql.sqltypes import GUID

from ...utils.date import now_datetime
from .base import BaseQuerySchema

if TYPE_CHECKING:
    from .order import Order
    from .user import User


class BaseClient(SQLModel):
    name: str = Field(..., description="Client name")
    email: EmailStr = Field(..., description="Client email")
    phone: constr(regex=r"^\d{2}9\d{8}$") = Field(..., description="Client cellphone")  # noqa

    @validator("name")
    def validate_name(cls, value: str) -> str:
        return value.title()


class CreateClient(BaseClient):
    pass


class UpdateClient(BaseClient):
    id: UUID = Field(..., description="Client ID")


class QueryClient(BaseQuerySchema):
    pass


class Client(BaseClient, table=True):
    __tablename__ = "clients"

    id: UUID = Field(default_factory=uuid4, description="Client ID", sa_column=Column("id", GUID(), primary_key=True))
    owner_id: UUID = Field(default_factory=uuid4, description="User ID that owns the client", foreign_key="users.id")
    created_at: datetime = Field(default_factory=now_datetime)

    owner: "User" = Relationship()
    orders: List["Order"] = Relationship(
        back_populates="client",
        sa_relationship_kwargs={"cascade": "all,delete", "lazy": "selectin", "passive_deletes": True},
    )
