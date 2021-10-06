import factory

from src.core.models.item import CreateItem


class CreateItemFactory(factory.Factory):
    image: bytes = factory.Faker("image")
    filename: str = factory.Faker("file_name", extension="png")
    code: str = factory.Faker("pystr", min_chars=10, max_chars=10)
    name: str = factory.Faker("word", locale="pt_BR")
    avaliable: bool = True
    buy_value: float = factory.Faker("pyfloat", positive=True, right_digits=2)
    sugested_sell_value: float = factory.LazyAttribute(lambda o: o.buy_value + (o.buy_value * 0.4))

    class Meta:
        model = CreateItem
