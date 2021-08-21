from .client import Streamer
from .elastic import ElasticStreamer


def default_streamer() -> Streamer:
    return ElasticStreamer()
