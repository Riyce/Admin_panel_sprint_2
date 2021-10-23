import logging
import os
import pathlib
import sqlite3

import psycopg2
from dotenv import load_dotenv
from psycopg2.extensions import connection as _connection
from psycopg2.extras import DictCursor

from sqlite_to_postgres.postgressaver import PostgresSaver
from sqlite_to_postgres.sqliteloader import SQLiteLoader
from sqlite_to_postgres.utils import TABLES_ARRAY

BASE_DIR = pathlib.Path(__file__).resolve().parent
load_dotenv(BASE_DIR.joinpath('.env.sample'))


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
        handlers=[logging.FileHandler(BASE_DIR.joinpath('logs/loader.log'))],
        level=logging.INFO,
        format='%(asctime)s | %(levelname)s - %(message)s',
    )
    dsl = {
        'dbname': os.environ.get('POSTGRES_DB'),
        'user': os.environ.get('POSTGRES_USER'),
        'password': os.environ.get('POSTGRES_PASSWORD'),
        'host': os.environ.get('POSTGRES_HOST'),
        'port': os.environ.get('POSTGRES_PORT')
    }
    batch_size = 500
    try:
        with (
            sqlite3.connect('db.sqlite') as sqlite_connection,
            psycopg2.connect(**dsl, cursor_factory=DictCursor) as pg_conn
        ):
            load_from_sqlite(sqlite_connection, pg_conn, batch_size)
        sqlite_connection.close()
        pg_conn.close()
    except psycopg2.OperationalError as error:
        logging.warning(
            f'Connection refused! {error}'
            f'Connection params {dsl}'
        )
        raise
