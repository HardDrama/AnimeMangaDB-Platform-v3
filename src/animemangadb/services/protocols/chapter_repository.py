"""
Chapter repository protocol.
"""

from __future__ import annotations

from typing import Protocol

from animemangadb.domain.entities import Chapter
from animemangadb.domain.value_objects.installment_identifier import (
    InstallmentIdentifier,
)
from animemangadb.domain.value_objects.slug import Slug


class ChapterRepositoryProtocol(Protocol):
    """
    Read-oriented protocol for Chapter repositories.
    """

    def get_by_identifier(
        self,
        series_slug: Slug,
        manga_title_slug: Slug,
        identifier: InstallmentIdentifier,
    ) -> Chapter | None:
        """
        Return one Chapter.
        """

    def list_for_manga_title(
        self,
        series_slug: Slug,
        manga_title_slug: Slug,
    ) -> list[Chapter]:
        """
        Return every Chapter belonging to one MangaTitle.
        """