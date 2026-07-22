"""Repository for Series aggregate roots."""

from __future__ import annotations

from sqlalchemy import select

from animemangadb.domain.entities.series import Series
from animemangadb.domain.value_objects.canonical_title import CanonicalTitle
from animemangadb.domain.value_objects.slug import Slug
from animemangadb.infrastructure.database.mappers.series_mapper import SeriesMapper
from animemangadb.infrastructure.database.models.series import SeriesORM

from .base import Repository


class SeriesRepository(Repository[SeriesORM]):
    """Persist and reconstruct Series domain entities."""

    orm_model = SeriesORM

    def add(self, domain_object: Series) -> Series:
        """Stage a new Series without committing the transaction."""
        if not isinstance(domain_object, Series):
            raise TypeError("domain_object must be a Series.")

        self._add(SeriesMapper.to_orm(domain_object))
        return domain_object

    def get_by_slug(self, slug: Slug) -> Series | None:
        """Return a Series by its domain slug."""
        self._validate_slug(slug)
        statement = select(SeriesORM).where(
            SeriesORM.slug == slug.value
        )
        orm_object = self._one_or_none(statement)
        return self._to_domain_or_none(orm_object)

    def get_by_title(
        self,
        title: CanonicalTitle,
    ) -> Series | None:
        """Return a Series by its canonical title."""
        self._validate_title(title)
        statement = select(SeriesORM).where(
            SeriesORM.title == title.value
        )
        orm_object = self._one_or_none(statement)
        return self._to_domain_or_none(orm_object)

    def exists_by_slug(self, slug: Slug) -> bool:
        """Return whether a Series with the slug exists."""
        self._validate_slug(slug)
        return self._exists(SeriesORM.slug == slug.value)

    def list_all(self) -> list[Series]:
        """Return all Series ordered by persistence identity."""
        statement = select(SeriesORM).order_by(SeriesORM.id)
        return [
            SeriesMapper.to_domain(orm_object)
            for orm_object in self._list(statement)
        ]

    def delete(self, domain_object: Series) -> bool:
        """Stage the matching Series for deletion if it exists."""
        if not isinstance(domain_object, Series):
            raise TypeError("domain_object must be a Series.")

        statement = select(SeriesORM).where(
            SeriesORM.slug == domain_object.slug.value
        )
        orm_object = self._one_or_none(statement)
        if orm_object is None:
            return False

        self._delete(orm_object)
        return True

    @staticmethod
    def _validate_slug(slug: Slug) -> None:
        if not isinstance(slug, Slug):
            raise TypeError("slug must be a Slug.")

    @staticmethod
    def _validate_title(title: CanonicalTitle) -> None:
        if not isinstance(title, CanonicalTitle):
            raise TypeError("title must be a CanonicalTitle.")

    @staticmethod
    def _to_domain_or_none(
        orm_object: SeriesORM | None,
    ) -> Series | None:
        if orm_object is None:
            return None
        return SeriesMapper.to_domain(orm_object)
