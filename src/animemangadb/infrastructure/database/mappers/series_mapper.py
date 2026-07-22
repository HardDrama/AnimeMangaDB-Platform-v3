"""Mapper for Series Domain and ORM objects."""

from __future__ import annotations

from animemangadb.domain.entities.series import Series
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


class SeriesMapper(Mapper[Series, SeriesORM]):
    """Perform shallow conversion for Series objects."""

    @staticmethod
    def to_domain(orm_object: SeriesORM) -> Series:
        """Create a new Series from scalar ORM state."""
        if not isinstance(orm_object, SeriesORM):
            raise TypeError(
                "orm_object must be a SeriesORM."
            )

        domain_object = Series(
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
    def to_orm(domain_object: Series) -> SeriesORM:
        """Create a new unattached SeriesORM from Domain state."""
        if not isinstance(domain_object, Series):
            raise TypeError(
                "domain_object must be a Series."
            )

        return SeriesORM(
            title=canonical_title_to_string(
                domain_object.title
            ),
            slug=slug_to_string(domain_object.slug),
        )
