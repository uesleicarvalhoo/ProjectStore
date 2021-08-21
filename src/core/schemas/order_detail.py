from pydantic import BaseModel, Field
from pydantic.types import PositiveFloat

from .base import BaseQuerySchema
from .item import Item


class BaseOrderDetail(BaseModel):
    item_id: int = Field(..., description="ID do cliente que realizou a compra")
    buy_value: PositiveFloat = Field(..., description="Valor de compra do Item")
    sell_value: PositiveFloat = Field(..., description="Valor de venda do item")


class CreateOrderDetail(BaseOrderDetail):
    pass


class OrderDetail(BaseOrderDetail):
    id: int = Field(..., description="ID da compra")
    order_id: int = Field(None, description="ID da ordem de compra")
    item: Item = Field(..., description="Descrição do item")

    class Config:
        orm_mode: bool = True


class GetOrderDetail(BaseQuerySchema):
    order_id: int = Field(None, description="ID da ordem de compra")
