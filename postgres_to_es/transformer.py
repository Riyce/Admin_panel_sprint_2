import logging
from typing import Generator, List

from models.genre import Genre
from models.filmvork import Filmwork
from models.person import Person, PersonFull
from utils import coroutine

logger = logging.getLogger('ETL')


class Transformer:
    FILMWORK_FIELDS = ['id', 'imdb_rating', 'title', 'description']
    FILMWORK_LIST_FIELDS = [
        'director', 'actors_names', 'writers_names', 'actors', 'writers', 'genre', 'directors', 'genres'
    ]
    PERSON_FIELDS = ['p_id', 'name']
    GENRE_FIELDS = ['g_id', 'genre_name']
    NESTED_ROLE_FIELD = {
        'actor': ['actors_names', 'actors'],
        'director': ['director', 'directors'],
        'writer': ['writers', 'writers_names']
    }

    def accumulate_extract_data_movies(self, extract_data: List) -> List[Filmwork]:
        filmwork_dict = dict()
        for row in extract_data:
            if row['id'] in filmwork_dict:
                filmwork = filmwork_dict[row['id']]
            else:
                filmwork = Filmwork()
                for list_field in self.FILMWORK_LIST_FIELDS:
                    setattr(filmwork, list_field, list())

            for filmwork_field in self.FILMWORK_FIELDS:
                if not getattr(filmwork, filmwork_field):
                    setattr(filmwork, filmwork_field, row[filmwork_field])

            genre = Genre()
            for genre_field in self.GENRE_FIELDS:
                setattr(genre, genre_field, row[genre_field])

            if genre.genre_name not in filmwork.genre:
                filmwork.genre.append(genre.genre_name)
                filmwork.genres.append(genre)

            person = Person()
            for person_field in self.PERSON_FIELDS:
                setattr(person, person_field, row[person_field])

            role = row['role']
            if role == 'actor':
                if person.name not in filmwork.actors_names:
                    filmwork.actors_names.append(person.name)
                    filmwork.actors.append(person)
            elif role == 'director':
                if person.name not in filmwork.director:
                    filmwork.director.append(person.name)
                    filmwork.directors.append(person)
            elif role == 'writer':
                if person.name not in filmwork.writers_names:
                    filmwork.writers_names.append(person.name)
                    filmwork.writers.append(person)
            filmwork_dict[row['id']] = filmwork
        return [filmwork for filmwork in filmwork_dict.values()]

    @staticmethod
    def accumulate_extract_data_genres(extract_data: List) -> List[Genre]:
        genre_list = list()
        for row in extract_data:
            genre_list.append(Genre(g_id=row['id'], genre_name=row['name']))
        return genre_list

    @staticmethod
    def accumulate_extract_data_persons(extract_data: List) -> List[PersonFull]:
        person_dict = dict()
        for row in extract_data:
            if row['id'] in person_dict:
                person = person_dict[row['id']]
            else:
                person = PersonFull()
                for list_field in ['roles', 'film_ids']:
                    setattr(person, list_field, list())

            for field in ['id', 'full_name']:
                if not getattr(person, field):
                    setattr(person, field, row[field])

            role = row.get('role')
            if role and role not in person.roles:
                person.roles.append(role)

            film_work_id = row.get('film_work_id')
            if film_work_id and film_work_id not in person.film_ids:
                person.film_ids.append(film_work_id)

            person_dict[row['id']] = person
        return [person for person in person_dict.values()]

    @coroutine
    def transform(self, index: str, generator: Generator) -> Generator:
        while extract_data := (yield):
            method = getattr(self, f'accumulate_extract_data_{index}')
            result = method(extract_data)
            logging.info(f'Collected {len(result)} records to load.')
            generator.send(result)
