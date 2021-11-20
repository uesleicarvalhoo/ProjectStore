import factory

from src.core.models.order_detail import CreateOrderDetail


class CreateOrderDetailFactory(factory.Factory):
    item_name: str = factory.Faker("word")
    value: float = factory.Faker("pyfloat", positive=True, right_digits=2)

    class Meta:
        model = CreateOrderDetail
