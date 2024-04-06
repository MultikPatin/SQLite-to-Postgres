from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class UUIDMixin:
    id: str


@dataclass(frozen=True)
class DescriptionMixin:
    description: str


@dataclass(frozen=True)
class CreatedMixin:
    created_at: datetime


@dataclass(frozen=True)
class TimeStampedMixin(CreatedMixin):
    updated_at: datetime


@dataclass(frozen=True)
class FilmWork(UUIDMixin, DescriptionMixin, TimeStampedMixin):
    title: str
    creation_date: datetime
    file_path: str
    rating: float
    type: str


@dataclass(frozen=True)
class Genre(UUIDMixin, DescriptionMixin, TimeStampedMixin):
    name: str


@dataclass(frozen=True)
class Person(UUIDMixin, TimeStampedMixin):
    full_name: str


@dataclass(frozen=True)
class GenreFilmWork(UUIDMixin, CreatedMixin):
    film_work_id: str
    genre_id: str


@dataclass(frozen=True)
class PersonFilmWork(UUIDMixin, CreatedMixin):
    film_work_id: str
    person_id: str
    role: str


def get_schema_by_table_name(table_name: str) -> type:
    match table_name.lower():
        case "film_work":
            return FilmWork
        case "genre":
            return Genre
        case "person":
            return Person
        case "genre_film_work":
            return GenreFilmWork
        case "person_film_work":
            return PersonFilmWork
        case _:
            raise ValueError(f"Unknown table name: {table_name}")
