import factory

from src.core.models.file import CreateFile


class CreateFileFactory(factory.Factory):
    bucket_key: str = factory.Faker("filename", extension="png")
    hash: str = factory.Faker("md5")

    class Meta:
        model = CreateFile
