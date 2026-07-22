"""Mapper for Episode Domain and ORM objects."""

from __future__ import annotations

from animemangadb.domain.entities.anime_title import AnimeTitle
from animemangadb.domain.entities.episode import Episode
from animemangadb.infrastructure.database.models.anime_title import (
    AnimeTitleORM,
)
from animemangadb.infrastructure.database.models.episode import (
    EpisodeORM,
)

from .base import Mapper
from .helpers import (
    canonical_title_from_string,
    canonical_title_to_string,
    installment_identifier_from_string,
    installment_identifier_to_string,
    slug_to_string,
    validate_derived_slug,
)


class EpisodeMapper(Mapper[Episode, EpisodeORM]):
    """Perform shallow conversion for Episode objects.

    The repository supplies the already-resolved AnimeTitle or
    AnimeTitleORM parent. This mapper performs no queries and does
    not recursively map the parent or chapter mappings.
    """

    @staticmethod
    def to_domain(
        orm_object: EpisodeORM,
        *,
        anime_title: AnimeTitle,
    ) -> Episode:
        """Create an Episode using a resolved Domain parent."""
        if not isinstance(orm_object, EpisodeORM):
            raise TypeError(
                "orm_object must be an EpisodeORM."
            )

        if not isinstance(anime_title, AnimeTitle):
            raise TypeError(
                "anime_title must be an AnimeTitle."
            )

        domain_object = Episode(
            anime_title=anime_title,
            identifier=installment_identifier_from_string(
                orm_object.identifier
            ),
            title=canonical_title_from_string(
                orm_object.title
            ),
        )

        validate_derived_slug(
            persisted_slug=orm_object.slug,
            derived_slug=domain_object.slug,
        )

        return domain_object

    @staticmethod
    def to_orm(
        domain_object: Episode,
        *,
        anime_title_orm: AnimeTitleORM,
    ) -> EpisodeORM:
        """Create an unattached EpisodeORM with a resolved parent."""
        if not isinstance(domain_object, Episode):
            raise TypeError(
                "domain_object must be an Episode."
            )

        if not isinstance(anime_title_orm, AnimeTitleORM):
            raise TypeError(
                "anime_title_orm must be an AnimeTitleORM."
            )

        return EpisodeORM(
            anime_title=anime_title_orm,
            identifier=installment_identifier_to_string(
                domain_object.identifier
            ),
            title=canonical_title_to_string(
                domain_object.title
            ),
            slug=slug_to_string(domain_object.slug),
        )
