"""Mapper for MangaTitle Domain and ORM objects."""

from __future__ import annotations

from animemangadb.domain.entities.manga_title import MangaTitle
from animemangadb.domain.entities.series import Series
from animemangadb.infrastructure.database.models.manga_title import (
    MangaTitleORM,
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


class MangaTitleMapper(Mapper[MangaTitle, MangaTitleORM]):
    """Perform shallow conversion for MangaTitle objects.

    The repository must provide the already-resolved parent Series
    or SeriesORM. The mapper does not query for or recursively map it.
    """

    @staticmethod
    def to_domain(
        orm_object: MangaTitleORM,
        *,
        series: Series,
    ) -> MangaTitle:
        """Create a MangaTitle using a resolved Domain parent."""
        if not isinstance(orm_object, MangaTitleORM):
            raise TypeError(
                "orm_object must be a MangaTitleORM."
            )

        if not isinstance(series, Series):
            raise TypeError(
                "series must be a Series."
            )

        domain_object = MangaTitle(
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
        domain_object: MangaTitle,
        *,
        series_orm: SeriesORM,
    ) -> MangaTitleORM:
        """Create a MangaTitleORM using a resolved ORM parent."""
        if not isinstance(domain_object, MangaTitle):
            raise TypeError(
                "domain_object must be a MangaTitle."
            )

        if not isinstance(series_orm, SeriesORM):
            raise TypeError(
                "series_orm must be a SeriesORM."
            )

        return MangaTitleORM(
            series=series_orm,
            title=canonical_title_to_string(
                domain_object.title
            ),
            slug=slug_to_string(domain_object.slug),
        )
