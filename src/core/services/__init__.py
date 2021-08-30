import inject

from ..config import ENVIRONMENT, settings
from ..constants import EnvironmentEnum
from .cache.vendor import CacheClient, NoneCache, RedisClient
from .storage.vendor import NoneStorage, Storage, StorageS3
from .streamer.vendor import ElasticStreamer, NoneStreamer, Streamer


def configure_cache(binder: inject.Binder) -> None:
    if ENVIRONMENT == EnvironmentEnum.testing:
        binder.bind_to_constructor(CacheClient, lambda: NoneCache())

    else:
        binder.bind_to_constructor(CacheClient, lambda: RedisClient(settings.CACHE))


def configure_storage(binder: inject.Binder) -> None:
    if ENVIRONMENT == EnvironmentEnum.testing:
        binder.bind_to_constructor(Storage, lambda: NoneStorage())

    else:
        binder.bind_to_constructor(Storage, lambda: StorageS3())


def configure_streamer(binder: inject.Binder) -> None:
    if ENVIRONMENT == EnvironmentEnum.testing:
        binder.bind_to_constructor(Streamer, lambda: NoneStreamer())

    else:
        binder.bind_to_constructor(Streamer, lambda: ElasticStreamer())


def configure_services(binder: inject.Binder) -> None:
    configure_cache(binder)
    configure_storage(binder)
    configure_streamer(binder)


inject.configure(configure_services)
