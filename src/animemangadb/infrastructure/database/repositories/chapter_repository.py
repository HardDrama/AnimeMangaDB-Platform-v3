"""Repository for Chapter entities."""

from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import selectinload

from animemangadb.domain.entities.chapter import Chapter
from animemangadb.domain.entities.manga_title import MangaTitle
from animemangadb.domain.value_objects.installment_identifier import InstallmentIdentifier
from animemangadb.domain.value_objects.slug import Slug
from animemangadb.infrastructure.database.mappers.chapter_mapper import ChapterMapper
from animemangadb.infrastructure.database.mappers.manga_title_mapper import MangaTitleMapper
from animemangadb.infrastructure.database.mappers.series_mapper import SeriesMapper
from animemangadb.infrastructure.database.models.chapter import ChapterORM
from animemangadb.infrastructure.database.models.manga_title import MangaTitleORM
from animemangadb.infrastructure.database.models.series import SeriesORM

from .base import Repository


class ChapterRepository(Repository[ChapterORM]):
    """Persist Chapters and compose their MangaTitle and Series graph."""

    orm_model = ChapterORM

    def add(self, domain_object: Chapter) -> Chapter:
        if not isinstance(domain_object, Chapter):
            raise TypeError("domain_object must be a Chapter.")
        manga_title_orm = self._resolve_manga_title_orm(domain_object.manga_title)
        self._add(ChapterMapper.to_orm(domain_object, manga_title_orm=manga_title_orm))
        return domain_object

    def get_by_identifier(self, series_slug: Slug, manga_title_slug: Slug, identifier: InstallmentIdentifier) -> Chapter | None:
        self._validate_scope(series_slug, manga_title_slug, identifier)
        statement = self._base_select().where(
            SeriesORM.slug == series_slug.value,
            MangaTitleORM.slug == manga_title_slug.value,
            ChapterORM.identifier == identifier.value,
        )
        return self._to_domain_or_none(self._one_or_none(statement))

    def exists_by_identifier(self, series_slug: Slug, manga_title_slug: Slug, identifier: InstallmentIdentifier) -> bool:
        self._validate_scope(series_slug, manga_title_slug, identifier)
        return self._session.scalar(self._base_select().where(
            SeriesORM.slug == series_slug.value,
            MangaTitleORM.slug == manga_title_slug.value,
            ChapterORM.identifier == identifier.value,
        ).limit(1)) is not None

    def list_for_manga_title(self, series_slug: Slug, manga_title_slug: Slug) -> list[Chapter]:
        self._validate_slug(series_slug, "series_slug")
        self._validate_slug(manga_title_slug, "manga_title_slug")
        statement = self._base_select().where(
            SeriesORM.slug == series_slug.value,
            MangaTitleORM.slug == manga_title_slug.value,
        ).order_by(ChapterORM.id)
        return [self._to_domain(row) for row in self._list(statement)]

    def delete(self, domain_object: Chapter) -> bool:
        if not isinstance(domain_object, Chapter):
            raise TypeError("domain_object must be a Chapter.")
        parent = domain_object.manga_title
        statement = self._base_select().where(
            SeriesORM.slug == parent.series.slug.value,
            MangaTitleORM.slug == parent.slug.value,
            ChapterORM.identifier == domain_object.identifier.value,
        )
        orm_object = self._one_or_none(statement)
        if orm_object is None:
            return False
        self._delete(orm_object)
        return True

    def _resolve_manga_title_orm(self, domain_object: MangaTitle) -> MangaTitleORM:
        statement = select(MangaTitleORM).join(MangaTitleORM.series).where(
            SeriesORM.slug == domain_object.series.slug.value,
            MangaTitleORM.slug == domain_object.slug.value,
        )
        orm_object = self._session.scalars(statement).one_or_none()
        if orm_object is None:
            raise LookupError("Chapter requires a persisted MangaTitle parent.")
        return orm_object

    @staticmethod
    def _base_select():
        return select(ChapterORM).join(ChapterORM.manga_title).join(MangaTitleORM.series).options(
            selectinload(ChapterORM.manga_title).selectinload(MangaTitleORM.series)
        )

    @staticmethod
    def _to_domain(orm_object: ChapterORM) -> Chapter:
        series = SeriesMapper.to_domain(orm_object.manga_title.series)
        manga_title = MangaTitleMapper.to_domain(orm_object.manga_title, series=series)
        return ChapterMapper.to_domain(orm_object, manga_title=manga_title)

    @classmethod
    def _to_domain_or_none(cls, orm_object: ChapterORM | None) -> Chapter | None:
        return None if orm_object is None else cls._to_domain(orm_object)

    @staticmethod
    def _validate_slug(value: Slug, name: str) -> None:
        if not isinstance(value, Slug):
            raise TypeError(f"{name} must be a Slug.")

    @classmethod
    def _validate_scope(cls, series_slug: Slug, manga_title_slug: Slug, identifier: InstallmentIdentifier) -> None:
        cls._validate_slug(series_slug, "series_slug")
        cls._validate_slug(manga_title_slug, "manga_title_slug")
        if not isinstance(identifier, InstallmentIdentifier):
            raise TypeError("identifier must be an InstallmentIdentifier.")
