from abc import ABC, abstractmethod
from datetime import timedelta
from typing import Any, Union


class CacheClient(ABC):
    @abstractmethod
    def get(self, name: str, key: str) -> Any:
        raise NotImplementedError

    @abstractmethod
    def set(self, name: str, key: str, value: str, expiration: Union[timedelta, int]) -> None:
        raise NotImplementedError

    @abstractmethod
    def delete(self, key: str) -> None:
        raise NotImplementedError

    def _get_final_name(self, name: str) -> str:
        raise NotImplementedError

    def _get_final_key(self, key: str) -> str:
        raise NotImplementedError
