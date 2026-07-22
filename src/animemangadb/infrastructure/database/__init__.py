"""Database infrastructure package."""

from .base import Base
from .config import (
    DATABASE_URL_ENVIRONMENT_VARIABLE,
    DEFAULT_SQLITE_URL,
    DatabaseConfig,
    load_database_config,
)
from .engine import create_database_engine
from .mappers import (
    DEFAULT_MAPPING_POLICY,
    Mapper,
    MappingPolicy,
)
from .models import (
    AnimeTitleORM,
    ChapterORM,
    EpisodeChapterMappingORM,
    EpisodeORM,
    MangaTitleORM,
    SeriesORM,
)
from .session import SessionFactory

__all__ = [
    "Base",
    "DatabaseConfig",
    "DEFAULT_SQLITE_URL",
    "DATABASE_URL_ENVIRONMENT_VARIABLE",
    "load_database_config",
    "create_database_engine",
    "SessionFactory",
    "SeriesORM",
    "AnimeTitleORM",
    "MangaTitleORM",
    "EpisodeORM",
    "ChapterORM",
    "EpisodeChapterMappingORM",
    "Mapper",
    "MappingPolicy",
    "DEFAULT_MAPPING_POLICY",
]
