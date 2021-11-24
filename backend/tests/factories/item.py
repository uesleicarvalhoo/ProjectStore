import factory

from src.core.models.item import CreateItem


class CreateItemFactory(factory.Factory):
    code: str = factory.Faker("pystr", min_chars=10, max_chars=10)
    name: str = factory.Faker("word", locale="pt_BR")
    cost: float = factory.Faker("pyfloat", positive=True, right_digits=2, max_value=1000)
    value: float = factory.LazyAttribute(lambda o: o.cost + (o.cost * 0.4))
    amount: int = factory.Faker("pyint", min_value=0)

    class Meta:
        model = CreateItem
