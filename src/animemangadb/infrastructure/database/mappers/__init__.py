"""Database mapper infrastructure and concrete mappers."""

from .anime_title_mapper import AnimeTitleMapper
from .base import Mapper
from .manga_title_mapper import MangaTitleMapper
from .series_mapper import SeriesMapper
from .strategy import DEFAULT_MAPPING_POLICY, MappingPolicy

__all__ = [
    "Mapper",
    "MappingPolicy",
    "DEFAULT_MAPPING_POLICY",
    "SeriesMapper",
    "AnimeTitleMapper",
    "MangaTitleMapper",
]
