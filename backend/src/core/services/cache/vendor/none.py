from datetime import timedelta
from typing import Union

from .. import CacheClient


class NoneCache(CacheClient):
    """
    Client que não executa nada, apenas implementa os metódos sem nenhuma ação
    conforme o design pattern: https://sourcemaking.com/design_patterns/null_object
    """

    def get(self, name: str, key: str) -> None:
        pass

    def set(self, name: str, key: str, value: str, expiration: Union[timedelta, int]) -> None:
        pass

    def delete(self, key: str) -> None:
        pass

    def _get_final_key(self, key: str) -> None:
        pass

    def _get_final_name(self, name: str) -> None:
        pass
