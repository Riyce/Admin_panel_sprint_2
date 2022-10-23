from typing import Optional
from uuid import UUID

from pydantic import Field

from models.base import Base as BaseModel
from models.genre import GenreBase
from models.person import PersonBase


class FilmworkName(BaseModel):
    id: UUID = Field(..., alias="uuid")
    title: str


class FilmworkBase(FilmworkName):
    imdb_rating: float


class FilmworkDetail(FilmworkBase):
    description: str
    genres: list[GenreBase] = []
    actors: list[PersonBase] = []
    writers: Optional[list[PersonBase]] = []
    directors: Optional[list[PersonBase]] = []
