import inject

from ..config import ENVIRONMENT, settings
from ..constants import EnvironmentEnum
from .broker.vendor import Broker, NoneBroker, SQSBroker
from .cache.vendor import CacheClient, NoneCache, RedisClient
from .storage.vendor import NoneStorage, Storage, StorageS3
from .streamer.vendor import BrokerStreamer, NoneStreamer, Streamer


def configure_broker(binder: inject.Binder) -> None:
    if ENVIRONMENT == EnvironmentEnum.testing:
        binder.bind_to_constructor(Broker, NoneBroker)
    else:
        binder.bind_to_constructor(Broker, SQSBroker)


def configure_cache(binder: inject.Binder) -> None:
    if ENVIRONMENT == EnvironmentEnum.testing:
        binder.bind_to_constructor(CacheClient, NoneCache)
    else:
        binder.bind_to_constructor(CacheClient, lambda: RedisClient(settings.CACHE_HOST))


def configure_storage(binder: inject.Binder) -> None:
    if ENVIRONMENT == EnvironmentEnum.testing:
        binder.bind_to_constructor(Storage, NoneStorage)
    else:
        binder.bind_to_constructor(Storage, StorageS3)


def configure_streamer(binder: inject.Binder) -> None:
    if ENVIRONMENT == EnvironmentEnum.testing:
        binder.bind_to_constructor(Streamer, NoneStreamer)
    else:
        binder.bind_to_constructor(Streamer, BrokerStreamer)


def configure_services(binder: inject.Binder) -> None:
    configure_broker(binder)
    configure_cache(binder)
    configure_storage(binder)
    configure_streamer(binder)


inject.configure(configure_services)
