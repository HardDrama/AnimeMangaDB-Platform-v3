"""
AnimeTitle repository protocol.

Application services depend on this protocol rather than a concrete
database implementation.
"""

from __future__ import annotations

from typing import Protocol

from animemangadb.domain.entities import AnimeTitle
from animemangadb.domain.value_objects.canonical_title import CanonicalTitle
from animemangadb.domain.value_objects.slug import Slug


class AnimeTitleRepositoryProtocol(Protocol):
    """
    Read-oriented protocol for AnimeTitle repositories.
    """

    def get_by_slug(
        self,
        series_slug: Slug,
        slug: Slug,
    ) -> AnimeTitle | None:
        """
        Return an AnimeTitle scoped to one Series.
        """

    def get_by_title(
        self,
        series_slug: Slug,
        title: CanonicalTitle,
    ) -> AnimeTitle | None:
        """
        Return an AnimeTitle by parent slug and canonical title.
        """

    def exists_by_slug(
        self,
        series_slug: Slug,
        slug: Slug,
    ) -> bool:
        """
        Return True when the scoped AnimeTitle exists.
        """

    def list_for_series(
        self,
        series_slug: Slug,
    ) -> list[AnimeTitle]:
        """
        Return all AnimeTitle entities belonging to one Series.
        """