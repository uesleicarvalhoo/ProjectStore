from datetime import date as date_
from typing import List

from pydantic import BaseModel
from sqlalchemy import Column, Enum
from sqlmodel import Field, Relationship, SQLModel

from ..constants import OrderEnum
from .base import BaseQuerySchema, common_relationship_kwargs
from .client import Client
from .order_detail import CreateOrderDetail, OrderDetail


class BaseOrder(SQLModel):
    client_id: int = Field(..., foreign_key="clients.id", description="ID do cliente que realizou a compra")
    date: date_ = Field(..., description="Data da venda")
    status: OrderEnum = Field(..., description="Status da venda", sa_column=Column(Enum(OrderEnum)))


class CreateOrder(BaseOrder):
    details: List["CreateOrderDetail"] = Field(..., description="Detalhes da venda")


class GetOrder(BaseQuerySchema):
    client_id: int = Field(None, description="ID do cliente")


class UpdateOrderStatus(BaseModel):
    order_id: int = Field(..., description="ID da venda")
    status: OrderEnum = Field(..., description="Status da venda")


class Order(BaseOrder, table=True):
    __tablename__ = "orders"

    id: int = Field(..., description="ID da venda", primary_key=True)

    client: "Client" = Relationship(back_populates="orders", sa_relationship_kwargs=common_relationship_kwargs)
    details: List["OrderDetail"] = Relationship(
        back_populates="order", sa_relationship_kwargs=common_relationship_kwargs
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
