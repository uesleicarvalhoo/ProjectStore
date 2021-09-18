from datetime import date as date_
from typing import List

from pydantic import BaseModel, Field

from ..constants import OrderEnum
from .base import BaseQuerySchema
from .order_detail import CreateOrderDetail, OrderDetail


class BaseOrder(BaseModel):
    client_id: int = Field(..., description="ID do cliente que realizou a compra")
    date: date_ = Field(..., description="Data da venda")
    status: OrderEnum = Field(..., description="Status da venda")


class CreateOrder(BaseOrder):
    details: List[CreateOrderDetail] = Field(..., description="Detalhes da venda", min_items=1)


class Order(BaseOrder):
    id: int = Field(..., description="ID da venda")
    details: List[OrderDetail] = Field(..., description="Descrição da ordem de venda")

    class Config:
        orm_mode: bool = True


class GetOrder(BaseQuerySchema):
    client_id: int = Field(None, description="ID do cliente")


class UpdateOrderStatus(BaseModel):
    order_id: int = Field(..., description="ID da venda")
    status: OrderEnum = Field(..., description="Status da venda")
