import string
from datetime import date
from random import choices, randint

from faker import Faker

faker = Faker()


def random_name() -> str:
    return faker.name()


def random_email() -> str:
    return faker.email()


def random_password() -> str:
    return faker.password()


def random_phone() -> str:
    return f"{randint(11, 99)}9{randint(80000000, 99999999)}"


def random_description(length: int = 5) -> str:
    return " ".join(faker.words(length))


def random_hash() -> str:
    return faker.md5()


def random_date() -> date:
    return faker.date_object()


def random_bucket_key() -> str:
    return f"{faker.uuid4()}.png"


def random_float_value() -> float:
    return faker.pyfloat(positive=True, max_value=1000, right_digits=2)


def random_lower_string() -> str:
    return "".join(choices(string.ascii_lowercase, k=32))


def random_filename(category: str, extension: str) -> str:
    return faker.file_name(category=category, extension=extension)
