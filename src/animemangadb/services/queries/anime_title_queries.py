"""
AnimeTitle query services.
"""

from __future__ import annotations

from animemangadb.domain.entities import AnimeTitle
from animemangadb.domain.value_objects.canonical_title import CanonicalTitle
from animemangadb.domain.value_objects.slug import Slug
from animemangadb.services.protocols import (
    AnimeTitleRepositoryProtocol,
)


class AnimeTitleQueryService:
    """
    Read-only application service for AnimeTitle entities.
    """

    def __init__(
        self,
        repository: AnimeTitleRepositoryProtocol,
    ) -> None:
        self._repository = repository

    def get_by_slug(
        self,
        series_slug: Slug,
        slug: Slug,
    ) -> AnimeTitle | None:
        """
        Retrieve an AnimeTitle scoped to one Series.
        """

        return self._repository.get_by_slug(
            series_slug,
            slug,
        )

    def get_by_title(
        self,
        series_slug: Slug,
        title: CanonicalTitle,
    ) -> AnimeTitle | None:
        """
        Retrieve an AnimeTitle by canonical title.
        """

        return self._repository.get_by_title(
            series_slug,
            title,
        )

    def list_for_series(
        self,
        series_slug: Slug,
    ) -> list[AnimeTitle]:
        """
        Retrieve all AnimeTitle entities for one Series.
        """

        return self._repository.list_for_series(
            series_slug,
        )