from typing import TYPE_CHECKING, Optional

from pydantic import PositiveFloat
from sqlmodel import Field, Relationship, SQLModel

from .base import BaseQuerySchema, common_relationship_kwargs

if TYPE_CHECKING:
    from .item import Item
    from .order import Order


class BaseOrderDetail(SQLModel):
    item_id: int = Field(foreign_key="items.id", description="ID do cliente que realizou a compra")
    buy_value: PositiveFloat = Field(description="Valor de compra do Item")
    sell_value: PositiveFloat = Field(description="Valor de venda do item")


class CreateOrderDetail(BaseOrderDetail):
    pass


class GetOrderDetail(BaseQuerySchema):
    order_id: int = Field(None, description="ID da ordem de compra")


class OrderDetail(BaseOrderDetail, table=True):
    __tablename__ = "order_details"

    id: int = Field(description="ID da compra", primary_key=True)
    order_id: Optional[int] = Field(description="ID da ordem de compra", foreign_key="orders.id")

    order: "Order" = Relationship(sa_relationship_kwargs=common_relationship_kwargs)
    item: "Item" = Relationship(sa_relationship_kwargs=common_relationship_kwargs)

    @property
    def profit(self) -> float:
        return self.sell_value - self.buy_value
