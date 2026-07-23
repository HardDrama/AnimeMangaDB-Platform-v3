"""
Episode query services.
"""

from __future__ import annotations

from animemangadb.domain.entities import Episode
from animemangadb.domain.value_objects.installment_identifier import (
    InstallmentIdentifier,
)
from animemangadb.domain.value_objects.slug import Slug
from animemangadb.services.protocols import (
    EpisodeRepositoryProtocol,
)


class EpisodeQueryService:
    """
    Read-only application service for Episodes.
    """

    def __init__(
        self,
        repository: EpisodeRepositoryProtocol,
    ) -> None:
        self._repository = repository

    def get_by_identifier(
        self,
        series_slug: Slug,
        anime_title_slug: Slug,
        identifier: InstallmentIdentifier,
    ) -> Episode | None:
        return self._repository.get_by_identifier(
            series_slug,
            anime_title_slug,
            identifier,
        )

    def list_for_anime_title(
        self,
        series_slug: Slug,
        anime_title_slug: Slug,
    ) -> list[Episode]:
        return self._repository.list_for_anime_title(
            series_slug,
            anime_title_slug,
        )