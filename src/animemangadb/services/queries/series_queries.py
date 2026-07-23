"""
Series query services.
"""

from __future__ import annotations

from animemangadb.domain.entities import Series
from animemangadb.domain.value_objects.slug import Slug
from animemangadb.services.protocols import (
    SeriesRepositoryProtocol,
)


class SeriesQueryService:
    """
    Read-only application service for Series.
    """

    def __init__(
        self,
        repository: SeriesRepositoryProtocol,
    ) -> None:
        self._repository = repository

    def get_by_slug(
        self,
        slug: Slug,
    ) -> Series | None:
        """
        Retrieve a Series by slug.
        """

        return self._repository.get_by_slug(slug)