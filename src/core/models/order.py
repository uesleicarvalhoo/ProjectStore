from datetime import date as date_
from typing import List
from uuid import UUID, uuid4

from pydantic import BaseModel
from sqlalchemy import Column, Enum
from sqlmodel import Field, Relationship, SQLModel

from ..constants import OrderEnum
from .base import BaseQuerySchema
from .client import Client
from .order_detail import CreateOrderDetail, OrderDetail
from .types import GUID


class BaseOrder(SQLModel):
    client_id: UUID = Field(..., foreign_key="clients.id", description="ID do cliente que realizou a compra")
    date: date_ = Field(..., description="Data da venda")
    status: OrderEnum = Field(..., description="Status da venda", sa_column=Column(Enum(OrderEnum)))


class CreateOrder(BaseOrder):
    details: List["CreateOrderDetail"] = Field(..., description="Detalhes da venda")


class GetOrder(BaseQuerySchema):
    client_id: UUID = Field(None, description="ID do cliente")


class UpdateOrderStatus(BaseModel):
    order_id: UUID = Field(..., description="ID da venda")
    status: OrderEnum = Field(..., description="Status da venda")


class Order(BaseOrder, table=True):
    __tablename__ = "orders"

    id: UUID = Field(
        default_factory=uuid4,
        description="ID da venda",
        sa_column=Column("id", GUID(), default=uuid4(), primary_key=True),
    )
    client: "Client" = Relationship(back_populates="orders")
    details: List["OrderDetail"] = Relationship(
        back_populates="order",
        sa_relationship_kwargs={"cascade": "all,delete", "lazy": "selectin", "passive_deletes": True},
    )

    @property
    def cost_total(self) -> float:
        return sum(detail.buy_value for detail in self.details)

    @property
    def sell_total(self) -> float:
        return sum(detail.sell_value for detail in self.details)

    @property
    def profit(self) -> float:
        return self.sell_total - self.cost_total
