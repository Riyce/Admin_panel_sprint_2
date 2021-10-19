from dataclasses import dataclass
from datetime import date, datetime


@dataclass
class Movie:
    id: str
    title: str
    description: str
    creation_date: date
    certificate: str
    file_path: str
    rating: float
    type: str
    created_at: datetime
    updated_at: datetime


@dataclass
class Genre:
    name: str
    description: str
    created_at: datetime
    updated_at: datetime
    id: str


@dataclass
class Person:
    id: str
    full_name: str
    birth_date: date
    created_at: datetime
    updated_at: datetime


@dataclass
class GenreFilm:
    id: str
    film_work_id: str
    genre_id: str
    created_at: datetime


@dataclass
class PersonFilm:
    id: str
    film_work_id: str
    person_id: str
    role: str
    created_at: datetime
