from .client import Streamer
from .elastic import ElasticStreamer

DefaultStreamer = ElasticStreamer()


def default_streamer() -> Streamer:
    return ElasticStreamer()
