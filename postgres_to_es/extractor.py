import logging
from datetime import datetime
from typing import Any, Dict, Generator, List, Union

import psycopg2

from backoff import backoff
from config import STATE_DIR
from state import JsonFileStorage, State
from utils import Entity, coroutine

PG_STATE_FILE = str(STATE_DIR.joinpath('{index}_postgre.json'))
logger = logging.getLogger('PostgreSQL')


class Extractor:
    def __init__(
            self,
            settings: Dict[str, str],
            index: str,
            source: Entity = None,
            query_size: int = 1,
    ) -> None:
        self.source = source
        self.settings = settings
        self.query_size = query_size
        self.state = State(JsonFileStorage(PG_STATE_FILE.format(index=index)))
        self.connection = psycopg2.connect(**self.settings)

    @backoff(logger)
    def __create_cursor(self):
        if self.connection:
            return self.connection.cursor()

    @backoff(logger)
    def __close_cursor(self, cursor) -> None:
        if not cursor.closed:
            cursor.close()

    def __set_start_time(self, last_record: Dict[str, Union[str, datetime]]) -> None:
        if self.source != Entity.INIT:
            self.state.set_state(self.source.value, str(last_record['updated_at']))

    def get_start_time(self) -> str:
        start_time = self.state.get_state(self.source.value)
        if not start_time:
            start_time = str(datetime.utcnow())
            self.state.set_state(self.source.value, start_time)
        return start_time

    @backoff(logger)
    def execute_many(self, query: str, query_params: List[str], generator: Generator):
        cursor = self.__create_cursor()
        if query_params:
            sql_query = cursor.mogrify(query, (tuple(query_params),))
        else:
            sql_query = query
        cursor.execute(sql_query)
        while True:
            columns = [col[0] for col in cursor.description]
            results = cursor.fetchmany(self.query_size)
            if not results:
                break
            generator.send([dict(zip(columns, row)) for row in results])
        self.__close_cursor(cursor)

    @backoff(logger)
    def execute_all(self, query: str, query_params: List[str]) -> List[Dict[str, Any]]:
        cursor = self.__create_cursor()
        sql_query = cursor.mogrify(query, (tuple(query_params),))
        cursor.execute(sql_query)
        columns = [col[0] for col in cursor.description]
        results = cursor.fetchall()
        self.__close_cursor(cursor)
        return [dict(zip(columns, row)) for row in results]

    @coroutine
    def extract(self, generator: Generator, query: str) -> Generator:
        while objs_ := (yield):
            self.__set_start_time(objs_[-1])
            generator.send(self.execute_all(query, [obj_['id'] for obj_ in objs_]))

    def extract_ids(self, generator: Generator, first_query: str, second_query: str = None):
        if second_query:
            results = self.execute_all(first_query, [self.get_start_time()])
            if results:
                self.__set_start_time(results[-1])
                self.execute_many(second_query, [result['id'] for result in results], generator)
        else:
            self.execute_many(first_query, [self.get_start_time()], generator)
