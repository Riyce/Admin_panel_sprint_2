from functools import lru_cache
from typing import Optional

from aioredis import Redis
from elasticsearch import AsyncElasticsearch
from fastapi import Depends

from core import config
from db.elasticsearch import get_elastic
from db.redis import get_redis
from models.filmwork import FilmworkBase, FilmworkDetail, FilmworkName
from services.base import BaseService
from services.cache import redis_cache


class FilmworkService(BaseService):
    INDEX = "movies"
    SEARCH_FIELDS = ["title", "description"]
    LITE_MODEL = FilmworkBase
    DETAIL_MODEL = FilmworkDetail
    LITE_MODEL_SOURCE_FIELDS = ["id", "title", "imdb_rating"]
    DETAIL_MODEL_SOURCE_FIELDS = [
        "id",
        "title",
        "imdb_rating",
        "description",
        "genres",
        "actors",
        "writers",
        "directors",
    ]

    @redis_cache(namespace="filmwork", ttl=config.REIDS_RECORD_LIVE_TIME)
    async def get_filmwork(self, uuid: str) -> Optional[FilmworkDetail]:
        filmworks = await self.get_obj(uuid)
        return filmworks

    @redis_cache(namespace="filmwork", ttl=config.REIDS_RECORD_LIVE_TIME)
    async def get_filmworks_list(self, **kwargs) -> list[FilmworkBase]:
        filmworks_objs = await self.get_obj_list(**kwargs)
        return filmworks_objs


@lru_cache()
def get_film_service(
    redis: Redis = Depends(get_redis),
    elastic: AsyncElasticsearch = Depends(get_elastic),
) -> FilmworkService:
    return FilmworkService(elastic, redis)
