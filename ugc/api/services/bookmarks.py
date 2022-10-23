import logging
from functools import lru_cache
from typing import Any, List
from uuid import uuid4

from core.config import config
from db.mongo import get_mongo_client
from fastapi import Depends
from models.bookmark import Bookmark, BookmarkFull
from motor.motor_asyncio import AsyncIOMotorClient

logger = logging.getLogger(__name__)


class BookmarkService:
    def __init__(self, mongo: AsyncIOMotorClient):
        self.mongo = mongo
        self.db = self.mongo[config.MONGO_DB]

    async def get_bookmarks(self, limit: int, skip: int, user_id: str) -> List[BookmarkFull]:
        collection = self.db[config.MONGO_BOOKMARKS_COLLECTION_NAME]
        bookmarks = []
        cursor = collection.find({"user_id": user_id})
        cursor.sort("time", -1).skip(skip).limit(limit)
        async for bookmark in collection.find({"user_id": user_id}):
            bookmark["id"] = bookmark.pop("_id")
            bookmarks.append(BookmarkFull(**bookmark))
        return bookmarks

    async def add_bookmark(self, bookmark: Bookmark) -> Any:
        collection = self.db[config.MONGO_BOOKMARKS_COLLECTION_NAME]
        bookmark_payload = bookmark.dict()
        bookmark_payload["_id"] = str(uuid4())
        bookmark = await collection.insert_one(bookmark_payload)
        return bookmark.inserted_id

    async def delete_bookmark(self, bookmark_id: str, user_id: str) -> None:
        collection = self.db[config.MONGO_BOOKMARKS_COLLECTION_NAME]
        await collection.delete_one({"_id": bookmark_id, "user_id": user_id})


@lru_cache()
def get_bookmark_service(
    mongo_storage: AsyncIOMotorClient = Depends(get_mongo_client),
) -> BookmarkService:
    return BookmarkService(mongo=mongo_storage)
