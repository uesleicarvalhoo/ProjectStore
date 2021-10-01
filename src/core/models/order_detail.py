from typing import TYPE_CHECKING, Optional
from uuid import UUID, uuid4

from pydantic import PositiveFloat
from sqlmodel import Column, Field, Relationship, SQLModel

from .base import BaseQuerySchema
from .types import GUID

if TYPE_CHECKING:
    from .item import Item
    from .order import Order


class BaseOrderDetail(SQLModel):
    item_id: UUID = Field(foreign_key="items.id", description="ID do cliente que realizou a compra")
    buy_value: PositiveFloat = Field(description="Valor de compra do Item")
    sell_value: PositiveFloat = Field(description="Valor de venda do item")


class CreateOrderDetail(BaseOrderDetail):
    pass


class GetOrderDetail(BaseQuerySchema):
    order_id: UUID = Field(None, description="ID da ordem de compra")


class OrderDetail(BaseOrderDetail, table=True):
    __tablename__ = "order_details"

    id: UUID = Field(
        default_factory=uuid4,
        description="ID do detalhamento",
        sa_column=Column("id", GUID(), default=uuid4(), primary_key=True),
    )
    order_id: Optional[UUID] = Field(description="ID da ordem de compra", foreign_key="orders.id")

    order: "Order" = Relationship(
        sa_relationship_kwargs={"cascade": "all,delete", "lazy": "selectin", "passive_deletes": True}
    )
    item: "Item" = Relationship()

    @property
    def profit(self) -> float:
        return self.sell_value - self.buy_value
