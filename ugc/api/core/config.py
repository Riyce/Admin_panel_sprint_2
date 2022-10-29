from logging import config as logging_config
from typing import List

from pydantic import BaseSettings


class Config(BaseSettings):
    MOVIE_PROGRESS_TOPIC: str = "views"
    MOVIE_ONLINE_TOPIC: str = "online"
    MOVIE_LIKE_TOPIC: str = "like"
    KAFKA_HOST: str = "localhost"
    KAFKA_PORT: int = 9092
    SECRET_KEY: str = "extra secret"
    HASH_ALGORITHM: str = "SHA-256"
    MONGO_HOST: str = "127.0.0.1"
    MONGO_PORT: int = 27017
    MONGO_DB: str = "ugc"
    MONGO_BOOKMARKS_COLLECTION_NAME = "bookmarks"
    MONGO_REVIEWS_COLLECTION_NAME = "reviews"
    MONGO_MOVIE_LIKES_COLLECTION_NAME = "movie_likes"
    MONGO_REVIEW_LIKES_COLLECTION_NAME = "review_likes"
    LOGSTASH_HOST: str = "localhost"
    LOGSTASH_PORT: int = 5044

    @property
    def kafka_uri(self) -> List[str]:
        return [f"{self.KAFKA_HOST}:{self.KAFKA_PORT}"]

    @property
    def mongo_uri(self) -> str:
        return f"mongodb://{self.MONGO_HOST}:{self.MONGO_PORT}"

    def get_collections(self) -> List[str]:
        return [
            self.MONGO_BOOKMARKS_COLLECTION_NAME,
            self.MONGO_REVIEWS_COLLECTION_NAME,
            self.MONGO_MOVIE_LIKES_COLLECTION_NAME,
            self.MONGO_REVIEW_LIKES_COLLECTION_NAME,
        ]


config = Config()
