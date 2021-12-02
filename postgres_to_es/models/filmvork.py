from dataclasses import dataclass
from typing import List

from models.genre import Genre
from models.person import Person


@dataclass
class Filmwork:
    id:            str = None
    imdb_rating:   float = None
    genre:         List[str] = None
    genres:        List[Genre] = None
    title:         str = None
    description:   str = None
    director:      List[str] = None
    actors_names:  List[str] = None
    writers_names: List[str] = None
    actors:        List[Person] = None
    writers:       List[Person] = None
    directors:     List[Person] = None

    def to_dict(self):
        return dict(
            id=self.id,
            imdb_rating=self.imdb_rating,
            genre=self.genre,
            genres=[genre_.to_dict() for genre_ in self.genres] if self.genres else None,
            title=self.title,
            description=self.description,
            director=self.director if self.director else None,
            actors_names=self.actors_names if self.actors_names else None,
            writers_names=self.writers_names if self.writers_names else None,
            actors=[prsn.to_dict() for prsn in self.actors] if self.actors else None,
            writers=[prsn.to_dict() for prsn in self.writers] if self.writers else None,
            directors=[prsn.to_dict() for prsn in self.directors] if self.directors else None,
        )
