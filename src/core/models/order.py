from datetime import date as date_
from typing import List, Optional
from uuid import UUID, uuid4

from pydantic import BaseModel
from pydantic.types import PositiveFloat
from sqlalchemy import Column, Enum
from sqlmodel import Field, Relationship, SQLModel
from sqlmodel.sql.sqltypes import GUID

from src.utils.date import now_datetime

from ..constants import OrderStatus, SaleType
from .client import Client
from .item import Item
from .order_detail import CreateOrderDetail, OrderDetail
from .user import User


class BaseOrder(SQLModel):
    client_id: UUID = Field(
        ..., foreign_key="clients.id", description="Identification of the customer who made purchase"
    )

    date: date_ = Field(..., description="Purchase date")
    status: OrderStatus = Field(..., description="Purchase Status", sa_column=Column(Enum(OrderStatus), nullable=False))
    description: Optional[str] = Field(description="Description of sale")
    sale_type: SaleType = Field(..., description="Tipo da operação", sa_column=Column(Enum(SaleType), nullable=False))


class CreateOrder(BaseOrder):
    items: List["CreateOrderDetail"] = Field(..., description="Details of purchase")
    date: date_ = Field(default_factory=lambda: now_datetime().date(), description="Purchase date")
    status: OrderStatus = Field(default=OrderStatus.PENDING, description="Purchase Status")


class QueryOrder(SQLModel):
    client_id: Optional[UUID] = Field(description="Identification of the customer who made purchase")
    status: Optional[OrderStatus] = Field(description="Purchase Status")
    start_date: Optional[date_] = Field(description="Initial date for query")
    end_date: Optional[date_] = Field(description="End date for query")


class UpdateOrderStatus(BaseModel):
    order_id: UUID = Field(..., description="Identification of Purchase")
    status: OrderStatus = Field(..., description="Purchase Status")


class Order(BaseOrder, table=True):
    __tablename__ = "orders"

    id: UUID = Field(
        default_factory=uuid4,
        description="Identification of Purchase",
        sa_column=Column("id", GUID(), primary_key=True),
    )
    owner_id: UUID = Field(..., description="User ID that owns the order", foreign_key="users.id")
    owner: User = Relationship()
    client: "Client" = Relationship(back_populates="orders")
    details: List["OrderDetail"] = Relationship(
        back_populates="order",
        sa_relationship_kwargs={"cascade": "all,delete", "lazy": "selectin", "passive_deletes": True},
    )

    @property
    def cost_total(self) -> float:
        return sum(detail.cost for detail in self.details)

    @property
    def sell_total(self) -> float:
        return sum(detail.sell_value for detail in self.details)

    @property
    def profit(self) -> float:
        return self.sell_total - self.cost_total

    @property
    def value(self) -> float:
        return self.sell_total

    @property
    def items(self) -> List[Item]:
        return [detail.item for detail in self.details]


class OrderResponse(BaseOrder):
    id: UUID = Field(
        ...,
        description="Identification of Purchase",
    )
    owner_id: UUID = Field(description="User ID that owns the order", foreign_key="users.id")
    owner: User
    client: Client
    details: List[OrderDetail]
    value: PositiveFloat
    items: List[Item]
