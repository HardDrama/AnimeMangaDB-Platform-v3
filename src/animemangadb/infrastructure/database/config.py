"""
Database configuration for AnimeMangaDB.
"""

from __future__ import annotations

import os
from dataclasses import dataclass


DEFAULT_SQLITE_URL = (
    "sqlite:///animemangadb.db"
)

DATABASE_URL_ENVIRONMENT_VARIABLE = (
    "ANIMEMANGADB_DATABASE_URL"
)


@dataclass(frozen=True)
class DatabaseConfig:
    """
    Immutable database configuration.

    This class contains only configuration values.

    It intentionally creates no SQLAlchemy engine,
    sessions, or database connections.
    """

    database_url: str


def load_database_config() -> DatabaseConfig:
    """
    Load database configuration from the environment.

    If the environment variable is not defined,
    a local SQLite URL is used.
    """

    database_url = os.getenv(
        DATABASE_URL_ENVIRONMENT_VARIABLE,
        DEFAULT_SQLITE_URL,
    )

    return DatabaseConfig(
        database_url=database_url,
    )