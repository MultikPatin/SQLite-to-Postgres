import os

from dotenv import load_dotenv
from psycopg2.extras import DictCursor

load_dotenv()

POSTGRES_DSL = {
    "dbname": os.environ.get("POSTGRES_DB"),
    "user": os.environ.get("POSTGRES_USER"),
    "password": os.environ.get("POSTGRES_PASSWORD"),
    "host": os.environ.get("POSTGRES_HOST", "127.0.0.1"),
    "port": os.environ.get("POSTGRES_PORT", 5432),
    "cursor_factory": DictCursor,
}
SQL_DB = os.environ.get("SQL_DB")

PG_INDEXES = {"film_work": ("creation_date",)}

TABLES = {
    "film_work": (
        ("id", "id"),
        ("title", "title"),
        ("description", "description"),
        ("creation_date", "creation_date"),
        ("file_path", None),
        ("rating", "rating"),
        ("type", "type"),
        ("created_at", "created"),
        ("updated_at", "modified"),
    ),
    "genre": (
        ("id", "id"),
        ("name", "name"),
        ("description", "description"),
        ("created_at", "created"),
        ("updated_at", "modified"),
    ),
    "person": (
        ("id", "id"),
        ("full_name", "full_name"),
        ("created_at", "created"),
        ("updated_at", "modified"),
    ),
    "genre_film_work": (
        ("id", "id"),
        ("film_work_id", "film_work_id"),
        ("genre_id", "genre_id"),
        ("created_at", "created"),
    ),
    "person_film_work": (
        ("id", "id"),
        ("film_work_id", "film_work_id"),
        ("person_id", "person_id"),
        ("role", "role"),
        ("created_at", "created"),
    ),
}

BUFFERED_ROWS = 100
