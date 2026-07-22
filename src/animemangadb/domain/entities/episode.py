"""
Domain entity representing an anime episode.
"""

from dataclasses import dataclass, field

from animemangadb.domain.entities.anime_title import AnimeTitle
from animemangadb.domain.exceptions import ValidationError
from animemangadb.domain.value_objects.canonical_title import (
    CanonicalTitle,
)
from animemangadb.domain.value_objects.installment_identifier import (
    InstallmentIdentifier,
)
from animemangadb.domain.value_objects.slug import Slug


@dataclass(eq=False)
class Episode:
    """
    Entity representing a single anime episode.
    """

    anime_title: AnimeTitle
    identifier: InstallmentIdentifier
    title: CanonicalTitle
    slug: Slug = field(init=False)

    def __post_init__(self) -> None:
        if not isinstance(self.anime_title, AnimeTitle):
            raise ValidationError(
                "Episode anime_title must be an AnimeTitle."
            )

        if not isinstance(
            self.identifier,
            InstallmentIdentifier,
        ):
            raise ValidationError(
                "Episode identifier must be an InstallmentIdentifier."
            )

        if not isinstance(
            self.title,
            CanonicalTitle,
        ):
            raise ValidationError(
                "Episode title must be a CanonicalTitle."
            )

        self.slug = Slug(self.title.value)

    def __str__(self) -> str:
        return (
            f"Episode {self.identifier}: "
            f"{self.title}"
        )