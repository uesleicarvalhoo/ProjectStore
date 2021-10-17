import factory

from src.core.models.file import CreateFile


class CreateFileFactory(factory.Factory):
    image: bytes = factory.Faker("image")
    filename: str = factory.Faker("file_name", extension="png")

    class Meta:
        model = CreateFile
