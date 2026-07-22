"""Repository for Episode entities."""

from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import selectinload

from animemangadb.domain.entities.anime_title import AnimeTitle
from animemangadb.domain.entities.episode import Episode
from animemangadb.domain.value_objects.installment_identifier import InstallmentIdentifier
from animemangadb.domain.value_objects.slug import Slug
from animemangadb.infrastructure.database.mappers.anime_title_mapper import AnimeTitleMapper
from animemangadb.infrastructure.database.mappers.episode_mapper import EpisodeMapper
from animemangadb.infrastructure.database.mappers.series_mapper import SeriesMapper
from animemangadb.infrastructure.database.models.anime_title import AnimeTitleORM
from animemangadb.infrastructure.database.models.episode import EpisodeORM
from animemangadb.infrastructure.database.models.series import SeriesORM

from .base import Repository


class EpisodeRepository(Repository[EpisodeORM]):
    """Persist Episodes and compose their AnimeTitle and Series graph."""

    orm_model = EpisodeORM

    def add(self, domain_object: Episode) -> Episode:
        if not isinstance(domain_object, Episode):
            raise TypeError("domain_object must be an Episode.")
        anime_title_orm = self._resolve_anime_title_orm(domain_object.anime_title)
        self._add(EpisodeMapper.to_orm(domain_object, anime_title_orm=anime_title_orm))
        return domain_object

    def get_by_identifier(
        self,
        series_slug: Slug,
        anime_title_slug: Slug,
        identifier: InstallmentIdentifier,
    ) -> Episode | None:
        self._validate_scope(series_slug, anime_title_slug, identifier)
        statement = self._base_select().where(
            SeriesORM.slug == series_slug.value,
            AnimeTitleORM.slug == anime_title_slug.value,
            EpisodeORM.identifier == identifier.value,
        )
        return self._to_domain_or_none(self._one_or_none(statement))

    def exists_by_identifier(
        self,
        series_slug: Slug,
        anime_title_slug: Slug,
        identifier: InstallmentIdentifier,
    ) -> bool:
        self._validate_scope(series_slug, anime_title_slug, identifier)
        return self._session.scalar(
            self._base_select().where(
                SeriesORM.slug == series_slug.value,
                AnimeTitleORM.slug == anime_title_slug.value,
                EpisodeORM.identifier == identifier.value,
            ).limit(1)
        ) is not None

    def list_for_anime_title(
        self,
        series_slug: Slug,
        anime_title_slug: Slug,
    ) -> list[Episode]:
        self._validate_slug(series_slug, "series_slug")
        self._validate_slug(anime_title_slug, "anime_title_slug")
        statement = self._base_select().where(
            SeriesORM.slug == series_slug.value,
            AnimeTitleORM.slug == anime_title_slug.value,
        ).order_by(EpisodeORM.id)
        return [self._to_domain(row) for row in self._list(statement)]

    def delete(self, domain_object: Episode) -> bool:
        if not isinstance(domain_object, Episode):
            raise TypeError("domain_object must be an Episode.")
        parent = domain_object.anime_title
        statement = self._base_select().where(
            SeriesORM.slug == parent.series.slug.value,
            AnimeTitleORM.slug == parent.slug.value,
            EpisodeORM.identifier == domain_object.identifier.value,
        )
        orm_object = self._one_or_none(statement)
        if orm_object is None:
            return False
        self._delete(orm_object)
        return True

    def _resolve_anime_title_orm(self, domain_object: AnimeTitle) -> AnimeTitleORM:
        statement = select(AnimeTitleORM).join(AnimeTitleORM.series).where(
            SeriesORM.slug == domain_object.series.slug.value,
            AnimeTitleORM.slug == domain_object.slug.value,
        )
        orm_object = self._session.scalars(statement).one_or_none()
        if orm_object is None:
            raise LookupError("Episode requires a persisted AnimeTitle parent.")
        return orm_object

    @staticmethod
    def _base_select():
        return select(EpisodeORM).join(EpisodeORM.anime_title).join(AnimeTitleORM.series).options(
            selectinload(EpisodeORM.anime_title).selectinload(AnimeTitleORM.series)
        )

    @staticmethod
    def _to_domain(orm_object: EpisodeORM) -> Episode:
        series = SeriesMapper.to_domain(orm_object.anime_title.series)
        anime_title = AnimeTitleMapper.to_domain(orm_object.anime_title, series=series)
        return EpisodeMapper.to_domain(orm_object, anime_title=anime_title)

    @classmethod
    def _to_domain_or_none(cls, orm_object: EpisodeORM | None) -> Episode | None:
        return None if orm_object is None else cls._to_domain(orm_object)

    @staticmethod
    def _validate_slug(value: Slug, name: str) -> None:
        if not isinstance(value, Slug):
            raise TypeError(f"{name} must be a Slug.")

    @classmethod
    def _validate_scope(cls, series_slug: Slug, anime_title_slug: Slug, identifier: InstallmentIdentifier) -> None:
        cls._validate_slug(series_slug, "series_slug")
        cls._validate_slug(anime_title_slug, "anime_title_slug")
        if not isinstance(identifier, InstallmentIdentifier):
            raise TypeError("identifier must be an InstallmentIdentifier.")
