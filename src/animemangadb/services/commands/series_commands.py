"""
Series command services.
"""

from __future__ import annotations

from animemangadb.domain.entities import Series
from animemangadb.domain.value_objects.canonical_title import CanonicalTitle
from animemangadb.services.exceptions import SeriesAlreadyExistsError
from animemangadb.services.protocols import (
    SeriesRepositoryProtocol,
    TransactionProtocol,
)


class SeriesCommandService:
    """
    Mutation-oriented application service for Series.
    """

    def __init__(
        self,
        repository: SeriesRepositoryProtocol,
        transaction: TransactionProtocol,
    ) -> None:
        self._repository = repository
        self._transaction = transaction

    def create(
        self,
        title: CanonicalTitle,
    ) -> Series:
        """
        Create and commit a Series with a unique derived slug.
        """

        try:
            series = Series(title)

            if self._repository.exists_by_slug(series.slug):
                raise SeriesAlreadyExistsError(series.slug)

            created_series = self._repository.add(series)
            self._transaction.commit()
        except Exception:
            self._transaction.rollback()
            raise

        return created_series
