"""Repository for MangaTitle entities."""

from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import selectinload

from animemangadb.domain.entities.manga_title import MangaTitle
from animemangadb.domain.value_objects.canonical_title import CanonicalTitle
from animemangadb.domain.value_objects.slug import Slug
from animemangadb.infrastructure.database.mappers.manga_title_mapper import (
    MangaTitleMapper,
)
from animemangadb.infrastructure.database.mappers.series_mapper import SeriesMapper
from animemangadb.infrastructure.database.models.manga_title import MangaTitleORM
from animemangadb.infrastructure.database.models.series import SeriesORM

from .base import Repository


class MangaTitleRepository(Repository[MangaTitleORM]):
    """Persist MangaTitle entities and compose their Series parent."""

    orm_model = MangaTitleORM

    def add(self, domain_object: MangaTitle) -> MangaTitle:
        """Stage a new MangaTitle using its persisted Series parent."""
        if not isinstance(domain_object, MangaTitle):
            raise TypeError("domain_object must be a MangaTitle.")

        series_orm = self._resolve_series_orm(
            domain_object.series.slug
        )
        self._add(
            MangaTitleMapper.to_orm(
                domain_object,
                series_orm=series_orm,
            )
        )
        return domain_object

    def get_by_slug(
        self,
        series_slug: Slug,
        slug: Slug,
    ) -> MangaTitle | None:
        """Return a MangaTitle by parent and title slugs."""
        self._validate_slug(series_slug, "series_slug")
        self._validate_slug(slug, "slug")
        statement = self._base_select().where(
            SeriesORM.slug == series_slug.value,
            MangaTitleORM.slug == slug.value,
        )
        return self._to_domain_or_none(
            self._one_or_none(statement)
        )

    def get_by_title(
        self,
        series_slug: Slug,
        title: CanonicalTitle,
    ) -> MangaTitle | None:
        """Return a MangaTitle by parent slug and canonical title."""
        self._validate_slug(series_slug, "series_slug")
        if not isinstance(title, CanonicalTitle):
            raise TypeError("title must be a CanonicalTitle.")
        statement = self._base_select().where(
            SeriesORM.slug == series_slug.value,
            MangaTitleORM.title == title.value,
        )
        return self._to_domain_or_none(
            self._one_or_none(statement)
        )

    def exists_by_slug(
        self,
        series_slug: Slug,
        slug: Slug,
    ) -> bool:
        """Return whether the scoped MangaTitle exists."""
        self._validate_slug(series_slug, "series_slug")
        self._validate_slug(slug, "slug")
        return self._session.scalar(
            self._base_select()
            .where(
                SeriesORM.slug == series_slug.value,
                MangaTitleORM.slug == slug.value,
            )
            .limit(1)
        ) is not None

    def list_for_series(
        self,
        series_slug: Slug,
    ) -> list[MangaTitle]:
        """Return MangaTitle entities for one Series."""
        self._validate_slug(series_slug, "series_slug")
        statement = (
            self._base_select()
            .where(SeriesORM.slug == series_slug.value)
            .order_by(MangaTitleORM.id)
        )
        return [
            self._to_domain(orm_object)
            for orm_object in self._list(statement)
        ]

    def delete(self, domain_object: MangaTitle) -> bool:
        """Stage the matching MangaTitle for deletion if present."""
        if not isinstance(domain_object, MangaTitle):
            raise TypeError("domain_object must be a MangaTitle.")
        statement = self._base_select().where(
            SeriesORM.slug == domain_object.series.slug.value,
            MangaTitleORM.slug == domain_object.slug.value,
        )
        orm_object = self._one_or_none(statement)
        if orm_object is None:
            return False
        self._delete(orm_object)
        return True

    def _resolve_series_orm(self, slug: Slug) -> SeriesORM:
        statement = select(SeriesORM).where(
            SeriesORM.slug == slug.value
        )
        series_orm = self._session.scalars(
            statement
        ).one_or_none()
        if series_orm is None:
            raise LookupError(
                "MangaTitle requires a persisted Series parent."
            )
        return series_orm

    @staticmethod
    def _validate_slug(slug: Slug, name: str) -> None:
        if not isinstance(slug, Slug):
            raise TypeError(f"{name} must be a Slug.")

    @staticmethod
    def _base_select():
        return (
            select(MangaTitleORM)
            .join(MangaTitleORM.series)
            .options(selectinload(MangaTitleORM.series))
        )

    @staticmethod
    def _to_domain(orm_object: MangaTitleORM) -> MangaTitle:
        series = SeriesMapper.to_domain(orm_object.series)
        return MangaTitleMapper.to_domain(
            orm_object,
            series=series,
        )

    @classmethod
    def _to_domain_or_none(
        cls,
        orm_object: MangaTitleORM | None,
    ) -> MangaTitle | None:
        if orm_object is None:
            return None
        return cls._to_domain(orm_object)
