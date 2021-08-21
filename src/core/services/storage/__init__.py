from .client import Storage
from .s3 import StorageS3


def default_storage() -> Storage:
    return StorageS3()
