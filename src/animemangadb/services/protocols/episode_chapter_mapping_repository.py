"""
Episode-chapter mapping repository protocol.
"""

from __future__ import annotations

from typing import Protocol

from animemangadb.domain.entities import (
    Chapter,
    Episode,
    EpisodeChapterMapping,
)


class EpisodeChapterMappingRepositoryProtocol(Protocol):
    """
    Read-oriented protocol for EpisodeChapterMapping repositories.

    The protocol describes the mapping queries consumed by the
    application-service layer without exposing SQLAlchemy details.
    """

    def get(
        self,
        episode: Episode,
        chapter: Chapter,
    ) -> EpisodeChapterMapping | None:
        """
        Return the mapping for one exact Episode-Chapter pair.
        """

    def exists(
        self,
        episode: Episode,
        chapter: Chapter,
    ) -> bool:
        """
        Return whether an exact Episode-Chapter mapping exists.
        """

    def list_for_episode(
        self,
        episode: Episode,
    ) -> list[EpisodeChapterMapping]:
        """
        Return every mapping associated with one Episode.
        """

    def list_for_chapter(
        self,
        chapter: Chapter,
    ) -> list[EpisodeChapterMapping]:
        """
        Return every mapping associated with one Chapter.
        """