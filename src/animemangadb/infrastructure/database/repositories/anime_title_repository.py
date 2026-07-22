"""Repository for AnimeTitle entities."""

from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import selectinload

from animemangadb.domain.entities.anime_title import AnimeTitle
from animemangadb.domain.value_objects.canonical_title import CanonicalTitle
from animemangadb.domain.value_objects.slug import Slug
from animemangadb.infrastructure.database.mappers.anime_title_mapper import (
    AnimeTitleMapper,
)
from animemangadb.infrastructure.database.mappers.series_mapper import SeriesMapper
from animemangadb.infrastructure.database.models.anime_title import AnimeTitleORM
from animemangadb.infrastructure.database.models.series import SeriesORM

from .base import Repository


class AnimeTitleRepository(Repository[AnimeTitleORM]):
    """Persist AnimeTitle entities and compose their Series parent."""

    orm_model = AnimeTitleORM

    def add(self, domain_object: AnimeTitle) -> AnimeTitle:
        """Stage a new AnimeTitle using its persisted Series parent."""
        if not isinstance(domain_object, AnimeTitle):
            raise TypeError("domain_object must be an AnimeTitle.")

        series_orm = self._resolve_series_orm(
            domain_object.series.slug
        )
        self._add(
            AnimeTitleMapper.to_orm(
                domain_object,
                series_orm=series_orm,
            )
        )
        return domain_object

    def get_by_slug(
        self,
        series_slug: Slug,
        slug: Slug,
    ) -> AnimeTitle | None:
        """Return an AnimeTitle by parent and title slugs."""
        self._validate_slug(series_slug, "series_slug")
        self._validate_slug(slug, "slug")
        statement = self._base_select().where(
            SeriesORM.slug == series_slug.value,
            AnimeTitleORM.slug == slug.value,
        )
        return self._to_domain_or_none(
            self._one_or_none(statement)
        )

    def get_by_title(
        self,
        series_slug: Slug,
        title: CanonicalTitle,
    ) -> AnimeTitle | None:
        """Return an AnimeTitle by parent slug and canonical title."""
        self._validate_slug(series_slug, "series_slug")
        if not isinstance(title, CanonicalTitle):
            raise TypeError("title must be a CanonicalTitle.")
        statement = self._base_select().where(
            SeriesORM.slug == series_slug.value,
            AnimeTitleORM.title == title.value,
        )
        return self._to_domain_or_none(
            self._one_or_none(statement)
        )

    def exists_by_slug(
        self,
        series_slug: Slug,
        slug: Slug,
    ) -> bool:
        """Return whether the scoped AnimeTitle exists."""
        self._validate_slug(series_slug, "series_slug")
        self._validate_slug(slug, "slug")
        return self._session.scalar(
            self._base_select()
            .where(
                SeriesORM.slug == series_slug.value,
                AnimeTitleORM.slug == slug.value,
            )
            .limit(1)
        ) is not None

    def list_for_series(
        self,
        series_slug: Slug,
    ) -> list[AnimeTitle]:
        """Return AnimeTitle entities for one Series."""
        self._validate_slug(series_slug, "series_slug")
        statement = (
            self._base_select()
            .where(SeriesORM.slug == series_slug.value)
            .order_by(AnimeTitleORM.id)
        )
        return [
            self._to_domain(orm_object)
            for orm_object in self._list(statement)
        ]

    def delete(self, domain_object: AnimeTitle) -> bool:
        """Stage the matching AnimeTitle for deletion if present."""
        if not isinstance(domain_object, AnimeTitle):
            raise TypeError("domain_object must be an AnimeTitle.")
        statement = self._base_select().where(
            SeriesORM.slug == domain_object.series.slug.value,
            AnimeTitleORM.slug == domain_object.slug.value,
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
                "AnimeTitle requires a persisted Series parent."
            )
        return series_orm

    @staticmethod
    def _validate_slug(slug: Slug, name: str) -> None:
        if not isinstance(slug, Slug):
            raise TypeError(f"{name} must be a Slug.")

    @staticmethod
    def _base_select():
        return (
            select(AnimeTitleORM)
            .join(AnimeTitleORM.series)
            .options(selectinload(AnimeTitleORM.series))
        )

    @staticmethod
    def _to_domain(orm_object: AnimeTitleORM) -> AnimeTitle:
        series = SeriesMapper.to_domain(orm_object.series)
        return AnimeTitleMapper.to_domain(
            orm_object,
            series=series,
        )

    @classmethod
    def _to_domain_or_none(
        cls,
        orm_object: AnimeTitleORM | None,
    ) -> AnimeTitle | None:
        if orm_object is None:
            return None
        return cls._to_domain(orm_object)
