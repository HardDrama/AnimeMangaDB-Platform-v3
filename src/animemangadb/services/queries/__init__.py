"""
Read-oriented application services.
"""

from .anime_title_queries import AnimeTitleQueryService
from .chapter_queries import ChapterQueryService
from .episode_queries import EpisodeQueryService
from .manga_title_queries import MangaTitleQueryService
from .mapping_queries import EpisodeChapterMappingQueryService
from .series_queries import SeriesQueryService

__all__ = [
    "AnimeTitleQueryService",
    "ChapterQueryService",
    "EpisodeChapterMappingQueryService",
    "EpisodeQueryService",
    "MangaTitleQueryService",
    "SeriesQueryService",
]