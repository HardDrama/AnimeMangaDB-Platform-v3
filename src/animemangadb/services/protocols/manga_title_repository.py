"""
MangaTitle repository protocol.

Application services depend on this protocol rather than a concrete
database implementation.
"""

from __future__ import annotations

from typing import Protocol

from animemangadb.domain.entities import MangaTitle
from animemangadb.domain.value_objects.canonical_title import CanonicalTitle
from animemangadb.domain.value_objects.slug import Slug


class MangaTitleRepositoryProtocol(Protocol):
    """
    Read-oriented protocol for MangaTitle repositories.
    """

    def get_by_slug(
        self,
        series_slug: Slug,
        slug: Slug,
    ) -> MangaTitle | None:
        """
        Return a MangaTitle scoped to one Series.
        """

    def get_by_title(
        self,
        series_slug: Slug,
        title: CanonicalTitle,
    ) -> MangaTitle | None:
        """
        Return a MangaTitle by parent slug and canonical title.
        """

    def exists_by_slug(
        self,
        series_slug: Slug,
        slug: Slug,
    ) -> bool:
        """
        Return True when the scoped MangaTitle exists.
        """

    def list_for_series(
        self,
        series_slug: Slug,
    ) -> list[MangaTitle]:
        """
        Return all MangaTitle entities belonging to one Series.
        """