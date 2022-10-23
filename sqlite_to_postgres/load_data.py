import logging
import os
import sqlite3

import psycopg2
from psycopg2.extensions import connection as _connection
from psycopg2.extras import DictCursor

from postgressaver import PostgresSaver
from sqliteloader import SQLiteLoader
from utils import TABLES_ARRAY


def load_from_sqlite(
        connection: sqlite3.Connection,
        pg_connection: _connection,
        batch: int
) -> None:
    postgres_saver = PostgresSaver(pg_connection)
    sqlite_loader = SQLiteLoader(connection, batch)
    for table in TABLES_ARRAY:
        sqlite_loader.get_table(table)
        has_data = True
        while has_data:
            data = sqlite_loader.load_data(table)
            has_data = bool(data)
            if has_data:
                postgres_saver.save_data_to_table(table, data)


if __name__ == '__main__':
    logging.basicConfig(
        handlers=[logging.FileHandler(__file__.replace('.py', '') + '.log')],
        level=logging.INFO,
        format='%(asctime)s | %(levelname)s - %(message)s',
    )
    dsl = {
        'dbname': os.environ.get('POSTGRES_DB', 'movies'),
        'user': os.environ.get('POSTGRES_USER', 'postgres'),
        'password': os.environ.get('POSTGRES_PASSWORD', 'postgres'),
        'host': os.environ.get('POSTGRES_HOST', 'localhost'),
        'port': os.environ.get('POSTGRES_PORT', 5432)
    }
    batch_size = 500
    try:
        with sqlite3.connect('db.sqlite') as sqlite_conn, psycopg2.connect(**dsl, cursor_factory=DictCursor) as pg_conn:
            load_from_sqlite(sqlite_conn, pg_conn, batch_size)
        sqlite_conn.close()
        pg_conn.close()
    except psycopg2.OperationalError as error:
        logging.warning(
            f'Connection refused! {error}'
            f'Connection params {dsl}'
        )
        raise
    print("OK. Data loaded.")
