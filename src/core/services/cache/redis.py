import pickle
from datetime import timedelta
from typing import Any, Union

from pydantic.networks import RedisDsn
from redis import Redis

from .client import CacheClient


class RedisClient(CacheClient):
    prefix: str
    client: Redis

    def __init__(self, config: RedisDsn, prefix: str = "") -> None:
        self.prefix = prefix
        self.client = Redis(config.host, config.port, 0, config.password)

    def get(self, name: str, key: str) -> Any:
        name = self._get_final_name(name)
        key = self._get_final_key(key)

        cached = self.client.hget(name, key)

        if not cached:
            return cached

        return pickle.loads(cached)

    def set(self, name: str, key: str, value: Any, expiration: Union[timedelta, int]) -> None:
        name = self._get_final_name(name)
        key = self._get_final_key(key)

        self.client.pipeline().hset(name, key, value=pickle.dumps(value)).expire(name, expiration).execute()

    def delete(self, key: str) -> None:
        self.client.delete(self._get_final_key(key))

    def _get_final_name(self, name: str) -> str:
        if self.prefix:
            return f"{self.prefix}-{name}"

        return name

    def _get_final_key(self, key: str) -> str:
        if self.prefix:
            return f"{self.prefix}-{key}"

        return key
