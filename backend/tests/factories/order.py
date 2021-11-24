from datetime import date as date_
from typing import List
from uuid import UUID

import factory

from src.core.constants import OrderStatus
from src.core.models.order import CreateOrder
from src.core.models.order_detail import CreateOrderDetail

from .order_detail import CreateOrderDetailFactory


class CreateOrderFactory(factory.Factory):
    client_id: UUID = factory.Faker("uuid4")
    date: factory.LazyFunction(date_.today)
    status: OrderStatus = OrderStatus.PENDING
    description: str = factory.Faker("sentence")
    items: List[CreateOrderDetail] = factory.List([factory.SubFactory(CreateOrderDetailFactory)])
    date: date_ = factory.LazyFunction(lambda: date_.today())

    class Meta:
        model = CreateOrder
