from sqlite3.dbapi2 import Connection as SQLiteConnection
from typing import Union

from psycopg2.extensions import connection as PGSQLConnection

from sqlite_to_postgres.models import (Genre, GenreFilm, Movie, Person,
                                       PersonFilm)
from sqlite_to_postgres.utils import Tables


class BaseSQLConnector:
    datatypes = {
        Tables.GENRE.value: Genre,
        Tables.GENREFILM.value: GenreFilm,
        Tables.MOVIE.value: Movie,
        Tables.PERSON.value: Person,
        Tables.PERSONFILM.value: PersonFilm
    }

    def __init__(
        self,
        connection: Union[SQLiteConnection, PGSQLConnection]
    ) -> None:
        self.cursor = connection.cursor()

    def get_datatype(
        self,
        table: str
    ) -> Union[Genre, GenreFilm, Movie, Person, PersonFilm]:
        return self.datatypes[table]
