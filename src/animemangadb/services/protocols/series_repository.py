"""
Series repository protocol.

Application services depend on this protocol rather than a concrete
database implementation.
"""

from __future__ import annotations

from typing import Protocol

from animemangadb.domain.entities import Series
from animemangadb.domain.value_objects.canonical_title import CanonicalTitle
from animemangadb.domain.value_objects.slug import Slug


class SeriesRepositoryProtocol(Protocol):
    """
    Persistence protocol for Series repositories.
    """

    def add(
        self,
        domain_object: Series,
    ) -> Series:
        """
        Stage a new Series and return the supplied domain entity.
        """

    def get_by_slug(
        self,
        slug: Slug,
    ) -> Series | None:
        """
        Return a Series matching the supplied slug.
        """

    def get_by_title(
        self,
        title: CanonicalTitle,
    ) -> Series | None:
        """
        Return a Series matching the supplied canonical title.
        """

    def exists_by_slug(
        self,
        slug: Slug,
    ) -> bool:
        """
        Return True when a matching Series exists.
        """

    def list_all(
        self,
    ) -> list[Series]:
        """
        Return all Series.
        """