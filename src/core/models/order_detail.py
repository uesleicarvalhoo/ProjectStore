from typing import TYPE_CHECKING, Optional
from uuid import UUID, uuid4

from pydantic import PositiveFloat
from pydantic.types import PositiveInt
from sqlmodel import Column, Field, Relationship, SQLModel
from sqlmodel.sql.sqltypes import GUID

if TYPE_CHECKING:
    from .item import Item
    from .order import Order


class BaseOrderDetail(SQLModel):
    item_id: UUID = Field(foreign_key="items.id", description="ID do cliente que realizou a compra")
    item_name: str = Field(description="Name of item")
    cost: float = Field(description="Value the item was purchased", ge=0)
    sell_value: PositiveFloat = Field(description="Value the item was sold")
    item_amount: PositiveInt = Field(description="Quantity of item")


class CreateOrderDetail(BaseOrderDetail):
    pass


class QueryOrderDetail(SQLModel):
    pass


class OrderDetail(BaseOrderDetail, table=True):
    __tablename__ = "order_details"

    id: UUID = Field(
        default_factory=uuid4, description="Identition of ID", sa_column=Column("id", GUID(), primary_key=True)
    )
    order_id: Optional[UUID] = Field(description="ID da ordem de compra", foreign_key="orders.id")

    order: "Order" = Relationship(
        sa_relationship_kwargs={"cascade": "all,delete", "lazy": "selectin", "passive_deletes": True}
    )
    item: "Item" = Relationship()

    @property
    def profit(self) -> float:
        return self.sell_value - self.cost
