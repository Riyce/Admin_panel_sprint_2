from typing import Any

from aioredis import Redis
from elasticsearch import AsyncElasticsearch
from pydantic import BaseModel

from services.connectors.elasticsearch import ElasticSearchConnector
from services.connectors.redis import RedisConnector


class BaseService:
    INDEX: str = None
    LITE_MODEL: BaseModel = None
    DETAIL_MODEL: BaseModel = None
    LITE_MODEL_SOURCE_FIELDS: list[str] = None
    DETAIL_MODEL_SOURCE_FIELDS: list[str] = None
    SEARCH_FIELDS: list[str] = None

    def __init__(self, es: AsyncElasticsearch, redis: Redis) -> None:
        self.es = ElasticSearchConnector(es)
        self.redis = RedisConnector(redis)

    async def get_obj(self, uuid: str) -> Any:
        result = await self.es.execute(index=self.INDEX, uuid=uuid, source=self.DETAIL_MODEL_SOURCE_FIELDS)
        hits = result["hits"]["hits"]
        obj_ = self.DETAIL_MODEL.parse_obj(hits[0]["_source"]) if hits else None
        return obj_

    async def get_obj_list(self, **kwargs) -> list[Any]:
        results = await self.es.execute(
            index=self.INDEX, query_search_fields=self.SEARCH_FIELDS, source=self.LITE_MODEL_SOURCE_FIELDS, **kwargs
        )
        objs = [self.LITE_MODEL.parse_obj(result["_source"]) for result in results["hits"]["hits"]]
        return objs
