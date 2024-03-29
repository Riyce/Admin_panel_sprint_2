import logging

from dataclasses import astuple, fields
from typing import List

from psycopg2 import DatabaseError
from base import BaseSQLConnector


class PostgresSaver(BaseSQLConnector):
    sql_template = """
        INSERT INTO content.{table} ({table_fields})
        VALUES {args}
        ON CONFLICT DO NOTHING
    """

    def save_data_to_table(self, table: str, data: List) -> None:
        input_rows = [astuple(row, tuple_factory=tuple) for row in data]
        fields_array = [
            field.name for field in fields(self.get_datatype(table))
        ]
        template = ', '.join(['%s'] * len(fields_array))
        args = ','.join(
            self.cursor.mogrify(
                f'({template})', row
            ).decode() for row in input_rows
        )
        table_fields = ','.join(fields_array)
        try:
            self.cursor.execute(self.sql_template.format(
                table=table,
                table_fields=table_fields,
                args=args
            ))
        except DatabaseError as e:
            logging.error(e)
