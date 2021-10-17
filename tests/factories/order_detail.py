import factory

from src.core.models.order_detail import CreateOrderDetail


class CreateOrderDetailFactory(factory.Factory):
    item_name: str = factory.Faker("word")
    cost: float = factory.Faker("pyfloat", positive=True, right_digits=2)
    sell_value: float = factory.LazyAttribute(lambda o: o.buy_value + (o.buy_value * 0.4))

    class Meta:
        model = CreateOrderDetail
