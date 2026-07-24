"""
Episode-Chapter mapping query services.
"""

from __future__ import annotations

from animemangadb.domain.entities import (
    Chapter,
    Episode,
    EpisodeChapterMapping,
)
from animemangadb.services.protocols import (
    EpisodeChapterMappingRepositoryProtocol,
)


class EpisodeChapterMappingQueryService:
    """
    Read-only application service for Episode-Chapter mappings.
    """

    def __init__(
        self,
        repository: EpisodeChapterMappingRepositoryProtocol,
    ) -> None:
        """
        Initialize the service with its mapping repository.
        """

        self._repository = repository

    def get(
        self,
        episode: Episode,
        chapter: Chapter,
    ) -> EpisodeChapterMapping | None:
        """
        Return the mapping for one exact Episode-Chapter pair.
        """

        return self._repository.get(
            episode,
            chapter,
        )

    def list_for_episode(
        self,
        episode: Episode,
    ) -> list[EpisodeChapterMapping]:
        """
        Return every mapping associated with one Episode.
        """

        return self._repository.list_for_episode(
            episode,
        )

    def list_for_chapter(
        self,
        chapter: Chapter,
    ) -> list[EpisodeChapterMapping]:
        """
        Return every mapping associated with one Chapter.
        """

        return self._repository.list_for_chapter(
            chapter,
        )