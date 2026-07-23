"""
MangaTitle query services.
"""

from __future__ import annotations

from animemangadb.domain.entities import MangaTitle
from animemangadb.domain.value_objects.canonical_title import CanonicalTitle
from animemangadb.domain.value_objects.slug import Slug
from animemangadb.services.protocols import (
    MangaTitleRepositoryProtocol,
)


class MangaTitleQueryService:
    """
    Read-only application service for MangaTitle entities.
    """

    def __init__(
        self,
        repository: MangaTitleRepositoryProtocol,
    ) -> None:
        self._repository = repository

    def get_by_slug(
        self,
        series_slug: Slug,
        slug: Slug,
    ) -> MangaTitle | None:
        """
        Retrieve a MangaTitle scoped to one Series.
        """

        return self._repository.get_by_slug(
            series_slug,
            slug,
        )

    def get_by_title(
        self,
        series_slug: Slug,
        title: CanonicalTitle,
    ) -> MangaTitle | None:
        """
        Retrieve a MangaTitle by canonical title.
        """

        return self._repository.get_by_title(
            series_slug,
            title,
        )

    def list_for_series(
        self,
        series_slug: Slug,
    ) -> list[MangaTitle]:
        """
        Retrieve all MangaTitle entities for one Series.
        """

        return self._repository.list_for_series(
            series_slug,
        )