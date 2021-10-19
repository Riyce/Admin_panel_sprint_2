import logging
from sqlite3 import OperationalError
from sqlite3.dbapi2 import Connection
from typing import List

from sqlite_to_postgres.base import BaseSQLConnector
from sqlite_to_postgres.utils import dict_factory


class SQLiteLoader(BaseSQLConnector):
    sql_template = """
        SELECT *
        FROM {table}
    """

    def __init__(
        self,
        connection: Connection,
        batch_size: int = 1000,
    ) -> None:
        super(SQLiteLoader, self).__init__(connection)
        self.batch_size = batch_size
        self.cursor.row_factory = dict_factory

    def get_table(self, table: str) -> None:
        try:
            self.cursor.execute(self.sql_template.format(table=table))
        except OperationalError:
            logging.warning(f'No such table - {table}.')
            raise

    def load_data(self, table: str) -> List:
        try:
            data_class = self.get_datatype(table)
        except KeyError:
            logging.warning(f'Unexpected table - {table}.')
            raise
        response = []
        results = self.cursor.fetchmany(self.batch_size)
        for result in results:
            try:
                obj = data_class(**result)
            except TypeError as e:
                logging.warning(f'Class {data_class.__name__} - {e}.')
                raise
            response.append(obj)
        return response
