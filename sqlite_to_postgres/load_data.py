import sqlite3

import psycopg2
from psycopg2.extensions import connection as _connection

from sqlite_to_postgres.config import POSTGRES_DSL, SQL_DB, TABLES
from sqlite_to_postgres.db.postgres import PostgresSaver
from sqlite_to_postgres.db.sqlite import SQLiteExtractor


def load_from_sqlite(connection: sqlite3.Connection, pg_conn: _connection):
    """Основной метод загрузки данных из SQLite в Postgres"""
    postgres_saver = PostgresSaver(pg_conn)
    sqlite_extractor = SQLiteExtractor(connection)

    for table_name in TABLES.keys():
        rows = sqlite_extractor.extract_table(table_name)
        postgres_saver.save_table(table_name, rows)


if __name__ == "__main__":
    with (
        sqlite3.connect(SQL_DB) as sqlite_conn,
        psycopg2.connect(**POSTGRES_DSL) as pg_conn,
    ):
        load_from_sqlite(sqlite_conn, pg_conn)
