"""Mapper for AnimeTitle Domain and ORM objects."""

from __future__ import annotations

from animemangadb.domain.entities.anime_title import AnimeTitle
from animemangadb.domain.entities.series import Series
from animemangadb.infrastructure.database.models.anime_title import (
    AnimeTitleORM,
)
from animemangadb.infrastructure.database.models.series import (
    SeriesORM,
)

from .base import Mapper
from .helpers import (
    canonical_title_from_string,
    canonical_title_to_string,
    slug_to_string,
    validate_derived_slug,
)


class AnimeTitleMapper(Mapper[AnimeTitle, AnimeTitleORM]):
    """Perform shallow conversion for AnimeTitle objects.

    The repository must provide the already-resolved parent Series
    or SeriesORM. The mapper does not query for or recursively map it.
    """

    @staticmethod
    def to_domain(
        orm_object: AnimeTitleORM,
        *,
        series: Series,
    ) -> AnimeTitle:
        """Create an AnimeTitle using a resolved Domain parent."""
        if not isinstance(orm_object, AnimeTitleORM):
            raise TypeError(
                "orm_object must be an AnimeTitleORM."
            )

        if not isinstance(series, Series):
            raise TypeError(
                "series must be a Series."
            )

        domain_object = AnimeTitle(
            series=series,
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
        domain_object: AnimeTitle,
        *,
        series_orm: SeriesORM,
    ) -> AnimeTitleORM:
        """Create an AnimeTitleORM using a resolved ORM parent."""
        if not isinstance(domain_object, AnimeTitle):
            raise TypeError(
                "domain_object must be an AnimeTitle."
            )

        if not isinstance(series_orm, SeriesORM):
            raise TypeError(
                "series_orm must be a SeriesORM."
            )

        return AnimeTitleORM(
            series=series_orm,
            title=canonical_title_to_string(
                domain_object.title
            ),
            slug=slug_to_string(domain_object.slug),
        )
