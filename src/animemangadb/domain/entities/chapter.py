"""
Domain entity representing a manga chapter.
"""

from dataclasses import dataclass, field

from animemangadb.domain.entities.manga_title import MangaTitle
from animemangadb.domain.exceptions import ValidationError
from animemangadb.domain.value_objects.canonical_title import (
    CanonicalTitle,
)
from animemangadb.domain.value_objects.installment_identifier import (
    InstallmentIdentifier,
)
from animemangadb.domain.value_objects.slug import Slug


@dataclass(eq=False)
class Chapter:
    """
    Entity representing a single manga chapter.
    """

    manga_title: MangaTitle
    identifier: InstallmentIdentifier
    title: CanonicalTitle
    slug: Slug = field(init=False)

    def __post_init__(self) -> None:
        if not isinstance(self.manga_title, MangaTitle):
            raise ValidationError(
                "Chapter manga_title must be a MangaTitle."
            )

        if not isinstance(
            self.identifier,
            InstallmentIdentifier,
        ):
            raise ValidationError(
                "Chapter identifier must be an InstallmentIdentifier."
            )

        if not isinstance(
            self.title,
            CanonicalTitle,
        ):
            raise ValidationError(
                "Chapter title must be a CanonicalTitle."
            )

        self.slug = Slug(self.title.value)

    def __str__(self) -> str:
        return (
            f"Chapter {self.identifier}: "
            f"{self.title}"
        )