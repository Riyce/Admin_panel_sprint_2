from functools import lru_cache
from typing import Optional

from aioredis import Redis
from elasticsearch import AsyncElasticsearch
from fastapi import Depends

from core import config
from db.elasticsearch import get_elastic
from db.redis import get_redis
from models.person import PersonDetail
from services.base import BaseService
from services.cache import redis_cache


class PersonService(BaseService):
    INDEX = "persons"
    SEARCH_FIELDS = ["full_name"]
    LITE_MODEL = PersonDetail
    DETAIL_MODEL = PersonDetail
    LITE_MODEL_SOURCE_FIELDS = ["id", "full_name", "roles", "film_ids"]
    DETAIL_MODEL_SOURCE_FIELDS = ["id", "full_name", "roles", "film_ids"]

    @redis_cache(namespace="person", ttl=config.REIDS_RECORD_LIVE_TIME)
    async def get_person(self, uuid: str) -> Optional[PersonDetail]:
        person_obj = await self.get_obj(uuid)
        return person_obj

    @redis_cache(namespace="person", ttl=config.REIDS_RECORD_LIVE_TIME)
    async def get_person_list(self, **kwargs) -> list[PersonDetail]:
        person_objs = await self.get_obj_list(**kwargs)
        return person_objs


@lru_cache()
def get_person_service(
    redis: Redis = Depends(get_redis),
    elastic: AsyncElasticsearch = Depends(get_elastic),
) -> PersonService:
    return PersonService(elastic, redis)
