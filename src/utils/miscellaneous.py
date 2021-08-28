import hashlib
from typing import Union

from src.core.config import settings
from src.core.services import RedisClient

cache = RedisClient(settings.CACHE)


def get_file_hash(file: Union[str, bytes]) -> Union[None, str]:
    file_data = file

    if isinstance(file, str):
        with open(file, "rb") as f:
            file_data = f.read()

    return hashlib.md5(file_data).hexdigest()
