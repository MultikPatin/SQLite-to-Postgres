![repo size](https://img.shields.io/github/repo-size/foxygen-d/cat_charity_fund)
![py version](https://img.shields.io/pypi/pyversions/3)
-----
[![Python](https://img.shields.io/badge/Python-3.9|3.10|3.11-blue?style=flat&logo=python&logoColor=white)](https://www.python.org/)
[![python-dotenv](https://img.shields.io/badge/dotenv-1.0.1-blue?style=flat&logo=python&logoColor=white)](https://pypi.org/project/python-dotenv/1.0.1)
[![psycopg2](https://img.shields.io/badge/psycopg2-2.9.9-blue?style=flat&logo=python&logoColor=white)](https://pypi.org/project/psycopg2/2.9.9/)

---
[![Poetry](https://img.shields.io/badge/Poetry-used-green?style=flat&logo=python&logoColor=white)](https://pypi.org/project/poetry/)
[![Ruff](https://img.shields.io/badge/Ruff-used-green?style=flat&logo=python&logoColor=white)](https://pypi.org/project/ruff/)


# SQLite-to-Postgres

Скрипт переноса данных из БД SQLite в БД Postgres


## Инструкция по развёртыванию проекта

* клонировать проект на компьютер
    ```bash
    git clone git@github.com:MultikPatin/SQLite-to-Postgres.git
    ```
* Установить менеджер зависимостей poetry
    ```bash
    python -m pip install poetry
    ```
* запуск виртуального окружения
    ```bash
    poetry shell
    ```
* установить зависимости
    ```bash
    poetry install --with dev
    ```
* запуск скрипта
    ```bash
    python -m sqlite_to_postgres.load_data
  ```