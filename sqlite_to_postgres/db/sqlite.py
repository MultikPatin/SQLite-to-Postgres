import sqlite3
from collections.abc import Generator

from sqlite_to_postgres.config import BUFFERED_ROWS
from sqlite_to_postgres.schemas.sqlite import get_schema_by_table_name
from sqlite_to_postgres.utils.logger import create_logger


class SQLiteExtractor:
    __table_name = None
    __cursor = None

    def __init__(self, connection: sqlite3.Connection):
        self.__connection = connection
        self.__connection.row_factory = sqlite3.Row
        self.logger = create_logger("SQLiteExtractor")

    def extract_table(self, table_name: str) -> Generator:
        self.__cursor = self.__connection.cursor()
        self.__table_name = table_name
        return self.__get_row_generator_by_table_name()

    def __get_row_generator_by_table_name(self) -> Generator:
        for rows in self.__get_data_from_table():
            for row in rows:
                yield get_schema_by_table_name(self.__table_name)(**dict(row))

    def __get_data_from_table(self) -> Generator:
        stmt = f"SELECT * FROM {self.__table_name}"
        try:
            self.__cursor.execute(stmt)
            self.logger.debug(stmt)
        except Exception as error:
            self.logger.error(
                f"==> При чтение данных из таблицы {self.__table_name} "
                f"возникла ошибка: {error}"
            )
        while True:
            rows = self.__cursor.fetchmany(BUFFERED_ROWS)
            if rows:
                yield rows
            else:
                self.__cursor.close()
                break
