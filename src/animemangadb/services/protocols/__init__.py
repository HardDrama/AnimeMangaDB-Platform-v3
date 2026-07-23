"""
Repository protocols consumed by application services.
"""

from .anime_title_repository import AnimeTitleRepositoryProtocol
from .chapter_repository import ChapterRepositoryProtocol
from .episode_repository import EpisodeRepositoryProtocol
from .manga_title_repository import MangaTitleRepositoryProtocol
from .series_repository import SeriesRepositoryProtocol

__all__ = [
    "AnimeTitleRepositoryProtocol",
    "ChapterRepositoryProtocol",
    "EpisodeRepositoryProtocol",
    "MangaTitleRepositoryProtocol",
    "SeriesRepositoryProtocol",
]