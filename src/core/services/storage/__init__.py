from .client import Storage
from .s3 import StorageS3

DefaultStorage = StorageS3()


def default_storage() -> Storage:
    return StorageS3()
