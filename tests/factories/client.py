from random import randint

import factory

from src.core.models.client import CreateClient


class CreateClientFactory(factory.Factory):
    name: str = factory.Faker("name", locale="pt_BR")
    email: str = factory.LazyAttribute(lambda o: "%s@example.com" % (o.name.lower().replace(" ", "_")))
    phone: str = factory.LazyFunction(lambda: f"{randint(11, 99)}9{randint(80000000, 99999999)}")

    class Meta:
        model = CreateClient
