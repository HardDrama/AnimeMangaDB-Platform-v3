"""
Domain entity representing an anime title.
"""

from dataclasses import dataclass, field

from animemangadb.domain.entities.series import Series
from animemangadb.domain.exceptions import ValidationError
from animemangadb.domain.value_objects.canonical_title import (
    CanonicalTitle,
)
from animemangadb.domain.value_objects.slug import Slug


@dataclass(eq=False)
class AnimeTitle:
    """
    Entity representing one anime title belonging to a Series.
    """

    series: Series
    title: CanonicalTitle
    slug: Slug = field(init=False)

    def __post_init__(self) -> None:
        if not isinstance(self.series, Series):
            raise ValidationError(
                "AnimeTitle series must be a Series."
            )

        if not isinstance(self.title, CanonicalTitle):
            raise ValidationError(
                "AnimeTitle title must be a CanonicalTitle."
            )

        self.slug = Slug(self.title.value)

    def __str__(self) -> str:
        return str(self.title)