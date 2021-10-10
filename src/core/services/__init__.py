import inject

from ..config import ENVIRONMENT, settings
from ..constants import EnvironmentEnum
from .broker.vendor import Broker, NoneBroker, SQSBroker
from .cache.vendor import CacheClient, NoneCache, RedisClient
from .email.vendor import BrokerEmailClient, EmailClient, NoneEmailClient, SMTPEmailClient
from .storage.vendor import NoneStorage, Storage, StorageS3
from .streamer.vendor import BrokerStreamer, ElasticStreamer, NoneStreamer, Streamer

if ENVIRONMENT == EnvironmentEnum.testing:
    DefaultCacheClient: CacheClient = lambda: NoneCache()
    DefaultStorage: Storage = lambda: NoneStorage()
    DefaultBroker: Broker = lambda: NoneBroker()
    DefaultStreamer: Streamer = lambda: NoneStreamer()
    DefaultEmailClient: EmailClient = lambda: NoneEmailClient()

else:
    DefaultCacheClient: CacheClient = lambda: RedisClient(settings.CACHE_HOST)
    DefaultStorage: Storage = lambda: StorageS3()
    DefaultBroker: Broker = lambda: SQSBroker()
    DefaultStreamer: Streamer = lambda: BrokerStreamer() if settings.STREAMER_USE_MESSAGE_BROKER else ElasticStreamer()
    DefaultEmailClient: EmailClient = (
        lambda: BrokerEmailClient if settings.EMAILS_USE_MESSAGE_BROKER else SMTPEmailClient()
    )


def configure_services(binder: inject.Binder) -> None:
    binder.bind_to_constructor(CacheClient, DefaultCacheClient)
    binder.bind_to_constructor(Storage, DefaultStorage)
    binder.bind_to_constructor(Streamer, DefaultStreamer)
    binder.bind_to_constructor(Broker, DefaultBroker)
    binder.bind_to_constructor(EmailClient, DefaultEmailClient)


inject.configure(configure_services)
