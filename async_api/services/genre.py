from functools import lru_cache
from typing import Optional

from aioredis import Redis
from elasticsearch import AsyncElasticsearch
from fastapi import Depends

from core import config
from db.elasticsearch import get_elastic
from db.redis import get_redis
from models.genre import GenreBase, GenreDetail
from services.base import BaseService
from services.cache import redis_cache


class GenreService(BaseService):
    INDEX = "genres"
    SEARCH_FIELDS = ["name"]
    LITE_MODEL = GenreBase
    DETAIL_MODEL = GenreDetail
    LITE_MODEL_SOURCE_FIELDS = ["id", "name"]
    DETAIL_MODEL_SOURCE_FIELDS = ["id", "name"]

    @redis_cache(namespace="genre", ttl=config.REIDS_RECORD_LIVE_TIME)
    async def get_genre(self, uuid: str) -> Optional[GenreDetail]:
        genre_obj = await self.get_obj(uuid)
        return genre_obj

    @redis_cache(namespace="genre", ttl=config.REIDS_RECORD_LIVE_TIME)
    async def get_genres_list(self, **kwargs) -> list[GenreBase]:
        genre_objs = await self.get_obj_list(**kwargs)
        return genre_objs


@lru_cache()
def get_genre_service(
    redis: Redis = Depends(get_redis),
    elastic: AsyncElasticsearch = Depends(get_elastic),
) -> GenreService:
    return GenreService(elastic, redis)
