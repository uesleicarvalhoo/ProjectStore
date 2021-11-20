from datetime import datetime
from typing import TYPE_CHECKING, List, Optional
from uuid import UUID, uuid4

from pydantic import EmailStr, constr, validator
from sqlmodel import Column, Field, Relationship, SQLModel
from sqlmodel.sql.sqltypes import GUID

from ...utils.date import now_datetime

if TYPE_CHECKING:
    from .order import Order
    from .user import User


class BaseClient(SQLModel):
    name: str = Field(..., description="Client name")
    email: Optional[EmailStr] = Field(description="Client email", nullable=True)
    phone: Optional[constr(regex=r"^\d{2}9\d{8}$")] = Field(..., description="Client cellphone", nullable=True)  # noqa
    zip_code: Optional[str] = Field(description="Postal code", nullable=True)
    address: Optional[str] = Field(description="Address of Client", nullable=True)

    @validator("name")
    def validate_name(cls, value: str) -> str:
        return value.title()


class CreateClient(BaseClient):
    pass


class UpdateClient(BaseClient):
    id: UUID = Field(..., description="Client ID")


class QueryClient(SQLModel):
    name: Optional[str] = Field(description="Name of client for query")


class Client(BaseClient, table=True):
    __tablename__ = "clients"

    id: UUID = Field(default_factory=uuid4, description="Client ID", sa_column=Column("id", GUID(), primary_key=True))
    owner_id: UUID = Field(..., description="User ID that owns the client", foreign_key="users.id")
    created_at: datetime = Field(default_factory=now_datetime)

    owner: "User" = Relationship()
    orders: List["Order"] = Relationship(
        back_populates="client",
        sa_relationship_kwargs={"cascade": "all,delete", "lazy": "selectin", "passive_deletes": True},
    )
