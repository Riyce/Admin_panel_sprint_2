import aioredis
import uvicorn
from elasticsearch import AsyncElasticsearch
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from api.v1 import filmworks, genres, persons
from core import config
from db import elasticsearch, redis

app = FastAPI(
    title=config.PROJECT_NAME,
    docs_url="/api/openapi",
    openapi_url="/api/openapi.json",
    default_response_class=ORJSONResponse,
    description="Information about movies, genres and people who participated in the creation of the work.",
    version="1.0.0",
)


@app.on_event("startup")
async def startup():
    redis.redis = await aioredis.create_redis_pool((config.REDIS_HOST, config.REDIS_PORT), minsize=10, maxsize=20)
    elasticsearch.es = AsyncElasticsearch(hosts=[f"{config.ELASTIC_HOST}:{config.ELASTIC_PORT}"])


@app.on_event("shutdown")
async def shutdown():
    await redis.redis.close()
    await elasticsearch.es.close()


app.include_router(filmworks.router, prefix="/api/v1/film", tags=["film"])
app.include_router(genres.router, prefix="/api/v1/genre", tags=["genre"])
app.include_router(persons.router, prefix="/api/v1/person", tags=["person"])


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8080,
    )
