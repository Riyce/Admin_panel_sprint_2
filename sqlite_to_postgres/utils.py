from enum import Enum


class Tables(Enum):
    GENRE = 'genre'
    PERSON = 'person'
    MOVIE = 'film_work'
    GENREFILM = 'genre_film_work'
    PERSONFILM = 'person_film_work'


TABLES_ARRAY = [
    Tables.GENRE.value, Tables.PERSON.value, Tables.MOVIE.value,
    Tables.GENREFILM.value, Tables.PERSONFILM.value
]


def dict_factory(cursor, row):
    result_dict = {}
    for idx, col in enumerate(cursor.description):
        result_dict[col[0]] = row[idx]
    return result_dict
