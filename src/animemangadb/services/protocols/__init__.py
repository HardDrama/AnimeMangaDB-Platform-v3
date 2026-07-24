"""
Repository and transaction protocols consumed by application services.
"""

from .anime_title_repository import AnimeTitleRepositoryProtocol
from .chapter_repository import ChapterRepositoryProtocol
from .episode_chapter_mapping_repository import (
    EpisodeChapterMappingRepositoryProtocol,
)
from .episode_repository import EpisodeRepositoryProtocol
from .manga_title_repository import MangaTitleRepositoryProtocol
from .series_repository import SeriesRepositoryProtocol
from .transaction import TransactionProtocol

__all__ = [
    "AnimeTitleRepositoryProtocol",
    "ChapterRepositoryProtocol",
    "EpisodeChapterMappingRepositoryProtocol",
    "EpisodeRepositoryProtocol",
    "MangaTitleRepositoryProtocol",
    "SeriesRepositoryProtocol",
    "TransactionProtocol",
]