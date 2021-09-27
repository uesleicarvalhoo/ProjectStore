from datetime import datetime
from typing import TYPE_CHECKING, List

from pydantic import EmailStr, constr, validator
from sqlmodel import Field, Relationship, SQLModel

from ...utils.date import now_datetime
from .base import BaseQuerySchema, common_relationship_kwargs

if TYPE_CHECKING:
    from .order import Order


class BaseClient(SQLModel):
    name: str = Field(..., description="Nome completo do cliente")
    email: EmailStr = Field(..., description="Email do cliente")
    phone: constr(regex=r"^\d{2}9\d{8}$") = Field(..., description="Telefone do cliente")  # noqa

    @validator("name")
    def validate_name(cls, value: str) -> str:
        return value.title()


class CreateClient(BaseClient):
    pass


class UpdateClient(BaseClient):
    id: int = Field(..., description="ID do Cliente")


class GetClient(BaseQuerySchema):
    id: int = Field(None, description="Id do cliente")
    name: str = Field(None, description="Nome do cliente")


class Client(BaseClient, table=True):
    __tablename__ = "clients"

    id: int = Field(..., description="ID do Cliente", primary_key=True)
    created_at: datetime = Field(default_factory=now_datetime)

    orders: List["Order"] = Relationship(back_populates="client", sa_relationship_kwargs=common_relationship_kwargs)
