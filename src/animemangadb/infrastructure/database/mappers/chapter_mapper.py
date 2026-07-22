"""Mapper for Chapter Domain and ORM objects."""

from __future__ import annotations

from animemangadb.domain.entities.chapter import Chapter
from animemangadb.domain.entities.manga_title import MangaTitle
from animemangadb.infrastructure.database.models.chapter import (
    ChapterORM,
)
from animemangadb.infrastructure.database.models.manga_title import (
    MangaTitleORM,
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


class ChapterMapper(Mapper[Chapter, ChapterORM]):
    """Perform shallow conversion for Chapter objects.

    The repository supplies the already-resolved MangaTitle or
    MangaTitleORM parent. This mapper performs no queries and does
    not recursively map the parent or episode mappings.
    """

    @staticmethod
    def to_domain(
        orm_object: ChapterORM,
        *,
        manga_title: MangaTitle,
    ) -> Chapter:
        """Create a Chapter using a resolved Domain parent."""
        if not isinstance(orm_object, ChapterORM):
            raise TypeError(
                "orm_object must be a ChapterORM."
            )

        if not isinstance(manga_title, MangaTitle):
            raise TypeError(
                "manga_title must be a MangaTitle."
            )

        domain_object = Chapter(
            manga_title=manga_title,
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
        domain_object: Chapter,
        *,
        manga_title_orm: MangaTitleORM,
    ) -> ChapterORM:
        """Create an unattached ChapterORM with a resolved parent."""
        if not isinstance(domain_object, Chapter):
            raise TypeError(
                "domain_object must be a Chapter."
            )

        if not isinstance(manga_title_orm, MangaTitleORM):
            raise TypeError(
                "manga_title_orm must be a MangaTitleORM."
            )

        return ChapterORM(
            manga_title=manga_title_orm,
            identifier=installment_identifier_to_string(
                domain_object.identifier
            ),
            title=canonical_title_to_string(
                domain_object.title
            ),
            slug=slug_to_string(domain_object.slug),
        )
