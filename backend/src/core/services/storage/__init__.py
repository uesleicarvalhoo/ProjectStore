from abc import ABC, abstractmethod
from typing import Union

DEFAULT_BUCKET = ...


class Storage(ABC):
    @abstractmethod
    def upload_file(self, file: Union[str, bytes], key: str, bucket: str = DEFAULT_BUCKET) -> str:
        raise NotImplementedError

    @abstractmethod
    def delete_file(self, key: str, bucket: str = DEFAULT_BUCKET) -> None:
        raise NotImplementedError

    @abstractmethod
    def check_file_exists(self, key: str, bucket: str = DEFAULT_BUCKET) -> bool:
        raise NotImplementedError
