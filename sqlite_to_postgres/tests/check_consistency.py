import sqlite3
import unittest
from datetime import datetime

import psycopg2

from sqlite_to_postgres.config import (
    POSTGRES_DSL,
    SQL_DB,
    TABLES,
)


class TestTableComparison(unittest.TestCase):
    def setUp(self):
        self.pg_conn = psycopg2.connect(**POSTGRES_DSL)
        self.sqlite_conn = sqlite3.connect(f"../{SQL_DB}")
        self.sqlite_conn.row_factory = sqlite3.Row

    def __get_sqlite_data_from_table(self, table: str) -> list:
        with self.sqlite_conn as sqlite_conn:
            stmt = f"SELECT * FROM {table}"
            return self.__get_data_from_table(stmt, sqlite_conn)

    def __get_sqlite_row_count_from_table(self, table: str) -> str:
        with self.sqlite_conn as sqlite_conn:
            stmt = f"SELECT COUNT(*) FROM {table}"
            res = self.__get_row_from_table(stmt, sqlite_conn)
            return dict(res)["COUNT(*)"]

    def __get_postgres_table_row_by_id(self, table: str, row_id: str) -> list:
        with self.pg_conn as pg_conn:
            stmt = f"SELECT * FROM content.{table} WHERE id='{row_id}'"
            return self.__get_data_from_table(stmt, pg_conn)[0]

    def __get_postgres_row_count_from_table(self, table: str) -> str:
        with self.pg_conn as pg_conn:
            stmt = f"SELECT COUNT(*) FROM content.{table}"
            return self.__get_row_from_table(stmt, pg_conn)[0]

    @staticmethod
    def __get_data_from_table(stmt: str, connection) -> list:
        cursor = connection.cursor()
        cursor.execute(stmt)
        res = cursor.fetchall()
        cursor.close()
        return res

    @staticmethod
    def __get_row_from_table(stmt: str, connection):
        cursor = connection.cursor()
        cursor.execute(stmt)
        res = cursor.fetchone()
        cursor.close()
        return res

    def __get_sqlite_rows_from_table_data(self, table_name: str, data: list):
        for sqlite_row in (dict(row) for row in data):
            row_id = sqlite_row.get("id")
            rows = self.__get_postgres_table_row_by_id(table_name, row_id)
            pg_row = dict(rows)
            yield sqlite_row, pg_row

    @staticmethod
    def __get_normalise_values(table_name: str, sqlite_row: dict, pg_row: dict):
        for sqlite_field, postgres_field in TABLES[table_name]:
            if postgres_field in ("created", "modified"):
                sqlite_value = datetime.strptime(
                    sqlite_row.get(sqlite_field).split("+")[0],
                    "%Y-%m-%d %H:%M:%S.%f",
                )
                postgres_value = pg_row.get(postgres_field).replace(tzinfo=None)
            else:
                sqlite_value = sqlite_row.get(sqlite_field)
                postgres_value = pg_row.get(postgres_field)
            yield sqlite_value, postgres_value

    def test_row_count_match_from_table_film_work(self):
        sqlite_count = self.__get_sqlite_row_count_from_table("film_work")
        pg_count = self.__get_postgres_row_count_from_table("film_work")
        self.assertEqual(sqlite_count, pg_count)

    def test_data_match_from_table_film_work(self):
        table_name = "film_work"
        sqlite_data = self.__get_sqlite_data_from_table(table_name)
        for sqlite_row, pg_row in self.__get_sqlite_rows_from_table_data(
            table_name, sqlite_data
        ):
            map(
                self.assertEqual,
                *self.__get_normalise_values(table_name, sqlite_row, pg_row),
            )

    def test_row_count_match_from_table_genre(self):
        sqlite_count = self.__get_sqlite_row_count_from_table("genre")
        pg_count = self.__get_postgres_row_count_from_table("genre")
        self.assertEqual(sqlite_count, pg_count)

    def test_data_match_from_table_genre(self):
        table_name = "genre"
        sqlite_data = self.__get_sqlite_data_from_table(table_name)
        for sqlite_row, pg_row in self.__get_sqlite_rows_from_table_data(
            table_name, sqlite_data
        ):
            map(
                self.assertEqual,
                *self.__get_normalise_values(table_name, sqlite_row, pg_row),
            )

    def test_row_count_match_from_table_person(self):
        sqlite_count = self.__get_sqlite_row_count_from_table("person")
        pg_count = self.__get_postgres_row_count_from_table("person")
        self.assertEqual(sqlite_count, pg_count)

    def test_data_match_from_table_person(self):
        table_name = "person"
        sqlite_data = self.__get_sqlite_data_from_table(table_name)
        for sqlite_row, pg_row in self.__get_sqlite_rows_from_table_data(
            table_name, sqlite_data
        ):
            map(
                self.assertEqual,
                *self.__get_normalise_values(table_name, sqlite_row, pg_row),
            )

    def test_row_count_match_from_table_genre_film_work(self):
        sqlite_count = self.__get_sqlite_row_count_from_table("genre_film_work")
        pg_count = self.__get_postgres_row_count_from_table("genre_film_work")
        self.assertEqual(sqlite_count, pg_count)

    def test_data_match_from_table_genre_film_work(self):
        table_name = "genre_film_work"
        sqlite_data = self.__get_sqlite_data_from_table(table_name)
        for sqlite_row, pg_row in self.__get_sqlite_rows_from_table_data(
            table_name, sqlite_data
        ):
            map(
                self.assertEqual,
                *self.__get_normalise_values(table_name, sqlite_row, pg_row),
            )

    def test_row_count_match_from_table_person_film_work(self):
        sqlite_count = self.__get_sqlite_row_count_from_table(
            "person_film_work"
        )
        pg_count = self.__get_postgres_row_count_from_table("person_film_work")
        self.assertEqual(sqlite_count, pg_count)

    def test_data_match_from_table_person_film_work(self):
        table_name = "person_film_work"
        sqlite_data = self.__get_sqlite_data_from_table(table_name)
        for sqlite_row, pg_row in self.__get_sqlite_rows_from_table_data(
            table_name, sqlite_data
        ):
            map(
                self.assertEqual,
                *self.__get_normalise_values(table_name, sqlite_row, pg_row),
            )
