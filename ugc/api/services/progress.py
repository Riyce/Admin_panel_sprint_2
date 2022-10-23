import json
import logging
from functools import lru_cache

from core.config import config
from db.kafka import KafkaHandler, get_kafka_handler
from fastapi import Depends
from models.progress import MovieProgress

logger = logging.getLogger(__name__)


class ProgressService:
    def __init__(self, storage: KafkaHandler):
        self.storage = storage

    @staticmethod
    def get_key(user_id: str, movie_id: str) -> bytes:
        return f"{user_id}::{movie_id}".encode()

    async def send_movie_progress(self, view_progress: MovieProgress) -> None:
        value = json.dumps(view_progress.dict()).encode()
        key = self.get_key(view_progress.user_id, view_progress.movie_id)
        await self.storage.send(topic=config.MOVIE_PROGRESS_TOPIC, value=value, key=key)

    async def send_movie_online(self, view_progress: MovieProgress) -> None:
        value = json.dumps(view_progress.get_movie_user()).encode()
        key = self.get_key(view_progress.user_id, view_progress.movie_id)
        await self.storage.send(topic=config.MOVIE_ONLINE_TOPIC, value=value, key=key)


@lru_cache()
def get_progress_service(
    event_storage: KafkaHandler = Depends(get_kafka_handler),
) -> ProgressService:
    return ProgressService(storage=event_storage)
