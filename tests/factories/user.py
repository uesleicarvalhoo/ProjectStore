import factory

from src.core.models.user import CreateUser


class CreateUserFactory(factory.Factory):
    name: str = factory.Faker("name", locale="pt_BR")
    email: str = factory.LazyAttribute(lambda o: "%s@example.com" % (o.name.lower().replace(" ", "_")))
    admin: bool = False
    password: str = factory.Faker("pystr", min_chars=5, max_chars=20)
    confirm_password: str = factory.LazyAttribute(lambda o: o.password)

    class Meta:
        model = CreateUser
