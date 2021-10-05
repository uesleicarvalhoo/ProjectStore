from datetime import date as date_
from typing import List
from uuid import UUID, uuid4

import factory

from src.core.constants import OrderEnum
from src.core.models.order import CreateOrder
from src.core.models.order_detail import CreateOrderDetail

from .order_detail import CreateOrderDetailFactory


class CreateOrderFactory(factory.Factory):
    client_id: UUID = factory.LazyFunction(uuid4)
    date: ...
    status: OrderEnum = OrderEnum.PENDING
    description: str = factory.Faker("sentence")
    details: List[CreateOrderDetail] = factory.List([factory.SubFactory(CreateOrderDetailFactory)])
    date: date_ = factory.LazyFunction(lambda: date_.today())

    class Meta:
        model = CreateOrder
