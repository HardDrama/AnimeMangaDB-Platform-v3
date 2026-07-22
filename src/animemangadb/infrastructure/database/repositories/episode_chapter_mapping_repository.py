"""Repository for EpisodeChapterMapping entities."""

from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import selectinload

from animemangadb.domain.entities.chapter import Chapter
from animemangadb.domain.entities.episode import Episode
from animemangadb.domain.entities.episode_chapter_mapping import EpisodeChapterMapping
from animemangadb.infrastructure.database.mappers.anime_title_mapper import AnimeTitleMapper
from animemangadb.infrastructure.database.mappers.chapter_mapper import ChapterMapper
from animemangadb.infrastructure.database.mappers.episode_chapter_mapping_mapper import EpisodeChapterMappingMapper
from animemangadb.infrastructure.database.mappers.episode_mapper import EpisodeMapper
from animemangadb.infrastructure.database.mappers.manga_title_mapper import MangaTitleMapper
from animemangadb.infrastructure.database.mappers.series_mapper import SeriesMapper
from animemangadb.infrastructure.database.models.anime_title import AnimeTitleORM
from animemangadb.infrastructure.database.models.chapter import ChapterORM
from animemangadb.infrastructure.database.models.episode import EpisodeORM
from animemangadb.infrastructure.database.models.episode_chapter_mapping import EpisodeChapterMappingORM
from animemangadb.infrastructure.database.models.manga_title import MangaTitleORM
from animemangadb.infrastructure.database.models.series import SeriesORM

from .base import Repository


class EpisodeChapterMappingRepository(Repository[EpisodeChapterMappingORM]):
    """Persist atomic Episode-to-Chapter relationships."""

    orm_model = EpisodeChapterMappingORM

    def add(self, domain_object: EpisodeChapterMapping) -> EpisodeChapterMapping:
        if not isinstance(domain_object, EpisodeChapterMapping):
            raise TypeError("domain_object must be an EpisodeChapterMapping.")
        episode_orm = self._resolve_episode_orm(domain_object.episode)
        chapter_orm = self._resolve_chapter_orm(domain_object.chapter)
        self._add(EpisodeChapterMappingMapper.to_orm(
            domain_object, episode_orm=episode_orm, chapter_orm=chapter_orm
        ))
        return domain_object

    def get(self, episode: Episode, chapter: Chapter) -> EpisodeChapterMapping | None:
        self._validate_related(episode, chapter)
        episode_orm = self._resolve_episode_orm(episode)
        chapter_orm = self._resolve_chapter_orm(chapter)
        orm_object = self._one_or_none(self._base_select().where(
            EpisodeChapterMappingORM.episode_id == episode_orm.id,
            EpisodeChapterMappingORM.chapter_id == chapter_orm.id,
        ))
        return self._to_domain_or_none(orm_object)

    def exists(self, episode: Episode, chapter: Chapter) -> bool:
        self._validate_related(episode, chapter)
        episode_orm = self._resolve_episode_orm(episode)
        chapter_orm = self._resolve_chapter_orm(chapter)
        return self._exists(
            EpisodeChapterMappingORM.episode_id == episode_orm.id,
            EpisodeChapterMappingORM.chapter_id == chapter_orm.id,
        )

    def list_for_episode(self, episode: Episode) -> list[EpisodeChapterMapping]:
        if not isinstance(episode, Episode):
            raise TypeError("episode must be an Episode.")
        episode_orm = self._resolve_episode_orm(episode)
        statement = self._base_select().where(
            EpisodeChapterMappingORM.episode_id == episode_orm.id
        ).order_by(EpisodeChapterMappingORM.id)
        return [self._to_domain(row) for row in self._list(statement)]

    def list_for_chapter(self, chapter: Chapter) -> list[EpisodeChapterMapping]:
        if not isinstance(chapter, Chapter):
            raise TypeError("chapter must be a Chapter.")
        chapter_orm = self._resolve_chapter_orm(chapter)
        statement = self._base_select().where(
            EpisodeChapterMappingORM.chapter_id == chapter_orm.id
        ).order_by(EpisodeChapterMappingORM.id)
        return [self._to_domain(row) for row in self._list(statement)]

    def delete(self, domain_object: EpisodeChapterMapping) -> bool:
        if not isinstance(domain_object, EpisodeChapterMapping):
            raise TypeError("domain_object must be an EpisodeChapterMapping.")
        episode_orm = self._resolve_episode_orm(domain_object.episode)
        chapter_orm = self._resolve_chapter_orm(domain_object.chapter)
        orm_object = self._one_or_none(select(EpisodeChapterMappingORM).where(
            EpisodeChapterMappingORM.episode_id == episode_orm.id,
            EpisodeChapterMappingORM.chapter_id == chapter_orm.id,
        ))
        if orm_object is None:
            return False
        self._delete(orm_object)
        return True

    def _resolve_episode_orm(self, episode: Episode) -> EpisodeORM:
        if not isinstance(episode, Episode):
            raise TypeError("episode must be an Episode.")
        statement = select(EpisodeORM).join(EpisodeORM.anime_title).join(AnimeTitleORM.series).where(
            SeriesORM.slug == episode.anime_title.series.slug.value,
            AnimeTitleORM.slug == episode.anime_title.slug.value,
            EpisodeORM.identifier == episode.identifier.value,
        )
        orm_object = self._session.scalars(statement).one_or_none()
        if orm_object is None:
            raise LookupError("Mapping requires a persisted Episode.")
        return orm_object

    def _resolve_chapter_orm(self, chapter: Chapter) -> ChapterORM:
        if not isinstance(chapter, Chapter):
            raise TypeError("chapter must be a Chapter.")
        statement = select(ChapterORM).join(ChapterORM.manga_title).join(MangaTitleORM.series).where(
            SeriesORM.slug == chapter.manga_title.series.slug.value,
            MangaTitleORM.slug == chapter.manga_title.slug.value,
            ChapterORM.identifier == chapter.identifier.value,
        )
        orm_object = self._session.scalars(statement).one_or_none()
        if orm_object is None:
            raise LookupError("Mapping requires a persisted Chapter.")
        return orm_object

    @staticmethod
    def _base_select():
        return select(EpisodeChapterMappingORM).options(
            selectinload(EpisodeChapterMappingORM.episode)
            .selectinload(EpisodeORM.anime_title)
            .selectinload(AnimeTitleORM.series),
            selectinload(EpisodeChapterMappingORM.chapter)
            .selectinload(ChapterORM.manga_title)
            .selectinload(MangaTitleORM.series),
        )

    @staticmethod
    def _to_domain(orm_object: EpisodeChapterMappingORM) -> EpisodeChapterMapping:
        episode_series = SeriesMapper.to_domain(orm_object.episode.anime_title.series)
        anime_title = AnimeTitleMapper.to_domain(orm_object.episode.anime_title, series=episode_series)
        episode = EpisodeMapper.to_domain(orm_object.episode, anime_title=anime_title)
        chapter_series = SeriesMapper.to_domain(orm_object.chapter.manga_title.series)
        manga_title = MangaTitleMapper.to_domain(orm_object.chapter.manga_title, series=chapter_series)
        chapter = ChapterMapper.to_domain(orm_object.chapter, manga_title=manga_title)
        return EpisodeChapterMappingMapper.to_domain(orm_object, episode=episode, chapter=chapter)

    @classmethod
    def _to_domain_or_none(cls, orm_object: EpisodeChapterMappingORM | None) -> EpisodeChapterMapping | None:
        return None if orm_object is None else cls._to_domain(orm_object)

    @staticmethod
    def _validate_related(episode: Episode, chapter: Chapter) -> None:
        if not isinstance(episode, Episode):
            raise TypeError("episode must be an Episode.")
        if not isinstance(chapter, Chapter):
            raise TypeError("chapter must be a Chapter.")
