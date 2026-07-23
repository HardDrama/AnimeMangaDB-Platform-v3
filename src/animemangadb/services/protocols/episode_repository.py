"""
Episode repository protocol.
"""

from __future__ import annotations

from typing import Protocol

from animemangadb.domain.entities import Episode
from animemangadb.domain.value_objects.installment_identifier import (
    InstallmentIdentifier,
)
from animemangadb.domain.value_objects.slug import Slug


class EpisodeRepositoryProtocol(Protocol):
    """
    Read-oriented protocol for Episode repositories.
    """

    def get_by_identifier(
        self,
        series_slug: Slug,
        anime_title_slug: Slug,
        identifier: InstallmentIdentifier,
    ) -> Episode | None:
        """
        Return one Episode.
        """

    def list_for_anime_title(
        self,
        series_slug: Slug,
        anime_title_slug: Slug,
    ) -> list[Episode]:
        """
        Return every Episode belonging to one AnimeTitle.
        """