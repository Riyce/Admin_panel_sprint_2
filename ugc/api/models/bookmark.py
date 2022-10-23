from datetime import datetime

from models.mixins import CreeateMixin
from pydantic import BaseModel


class BookmarkBase(BaseModel):
    movie_id: str


class Bookmark(BookmarkBase, CreeateMixin):
    user_id: str
    time: datetime


class BookmarkFull(Bookmark):
    id: str
