from uuid import UUID

import factory

from src.core.models.order_detail import CreateOrderDetail


class CreateOrderDetailFactory(factory.Factory):
    item_id: UUID = factory.Faker("uuid4")
    buy_value: float = factory.Faker("pyfloat", positive=True, right_digits=2)
    sell_value: float = factory.LazyAttribute(lambda o: o.buy_value + (o.buy_value * 0.4))

    class Meta:
        model = CreateOrderDetail
