"""
Chapter query services.
"""

from __future__ import annotations

from animemangadb.domain.entities import Chapter
from animemangadb.domain.value_objects.installment_identifier import (
    InstallmentIdentifier,
)
from animemangadb.domain.value_objects.slug import Slug
from animemangadb.services.protocols import (
    ChapterRepositoryProtocol,
)


class ChapterQueryService:
    """
    Read-only application service for Chapters.
    """

    def __init__(
        self,
        repository: ChapterRepositoryProtocol,
    ) -> None:
        self._repository = repository

    def get_by_identifier(
        self,
        series_slug: Slug,
        manga_title_slug: Slug,
        identifier: InstallmentIdentifier,
    ) -> Chapter | None:
        return self._repository.get_by_identifier(
            series_slug,
            manga_title_slug,
            identifier,
        )

    def list_for_manga_title(
        self,
        series_slug: Slug,
        manga_title_slug: Slug,
    ) -> list[Chapter]:
        return self._repository.list_for_manga_title(
            series_slug,
            manga_title_slug,
        )