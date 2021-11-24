import factory

from src.core.models.balance import CreateBalance


class CreateBalanceFactory(factory.Factory):
    value: float = factory.Faker("pyfloat", positive=True)
    description: str = factory.Faker("sentence", locale="pt_BR")

    class Meta:
        model = CreateBalance
