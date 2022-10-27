import uvicorn
# from core.sentry_fastapi import sentry_init
from db import kafka, mongo
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from api.v1.bookmark import router as bookmark_router
from api.v1.progress import router as progress_router
from api.v1.rating import router as rating_router

# sentry_init()
app = FastAPI(
    title="UGC API",
    docs_url="/ugc/apidocs",
    openapi_url="/ugc/apidocs.json",
    default_response_class=ORJSONResponse,
)

app.include_router(progress_router, prefix="/ugc/v1")
app.include_router(rating_router, prefix="/ugc/v1")
app.include_router(bookmark_router, prefix="/ugc/v1")


@app.on_event("startup")
async def startup_event():
    kafka.kafka_handler = await kafka.get_kafka_handler()
    mongo.mongo_client = await mongo.get_mongo()
    await mongo.init_collections()


@app.on_event("shutdown")
async def shutdown_event():
    await kafka.kafka_handler.stop()


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080)
