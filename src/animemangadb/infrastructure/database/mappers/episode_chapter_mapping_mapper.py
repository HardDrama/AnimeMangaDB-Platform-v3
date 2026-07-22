"""Mapper for EpisodeChapterMapping Domain and ORM objects."""

from __future__ import annotations

from animemangadb.domain.entities.chapter import Chapter
from animemangadb.domain.entities.episode import Episode
from animemangadb.domain.entities.episode_chapter_mapping import (
    EpisodeChapterMapping,
)
from animemangadb.infrastructure.database.models.chapter import (
    ChapterORM,
)
from animemangadb.infrastructure.database.models.episode import (
    EpisodeORM,
)
from animemangadb.infrastructure.database.models.episode_chapter_mapping import (
    EpisodeChapterMappingORM,
)

from .base import Mapper


class EpisodeChapterMappingMapper(
    Mapper[
        EpisodeChapterMapping,
        EpisodeChapterMappingORM,
    ]
):
    """Perform shallow conversion for atomic mapping objects.

    Both related entities must already be resolved. The mapper does
    not query, recursively map either branch, or copy persistence
    identity into the Domain object.
    """

    @staticmethod
    def to_domain(
        orm_object: EpisodeChapterMappingORM,
        *,
        episode: Episode,
        chapter: Chapter,
    ) -> EpisodeChapterMapping:
        """Create a Domain mapping from resolved related entities."""
        if not isinstance(
            orm_object,
            EpisodeChapterMappingORM,
        ):
            raise TypeError(
                "orm_object must be an "
                "EpisodeChapterMappingORM."
            )

        if not isinstance(episode, Episode):
            raise TypeError(
                "episode must be an Episode."
            )

        if not isinstance(chapter, Chapter):
            raise TypeError(
                "chapter must be a Chapter."
            )

        return EpisodeChapterMapping(
            episode=episode,
            chapter=chapter,
        )

    @staticmethod
    def to_orm(
        domain_object: EpisodeChapterMapping,
        *,
        episode_orm: EpisodeORM,
        chapter_orm: ChapterORM,
    ) -> EpisodeChapterMappingORM:
        """Create an unattached ORM mapping from resolved parents."""
        if not isinstance(
            domain_object,
            EpisodeChapterMapping,
        ):
            raise TypeError(
                "domain_object must be an "
                "EpisodeChapterMapping."
            )

        if not isinstance(episode_orm, EpisodeORM):
            raise TypeError(
                "episode_orm must be an EpisodeORM."
            )

        if not isinstance(chapter_orm, ChapterORM):
            raise TypeError(
                "chapter_orm must be a ChapterORM."
            )

        return EpisodeChapterMappingORM(
            episode=episode_orm,
            chapter=chapter_orm,
        )
