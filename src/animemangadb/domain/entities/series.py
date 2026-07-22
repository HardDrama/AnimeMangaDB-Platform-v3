"""
Domain entity representing a media series.
"""

from dataclasses import dataclass, field

from animemangadb.domain.exceptions import ValidationError
from animemangadb.domain.value_objects.canonical_title import (
    CanonicalTitle,
)
from animemangadb.domain.value_objects.slug import Slug


@dataclass(eq=False)
class Series:
    """
    Aggregate root representing one media series.

    A Series is identified in the domain by its own lifecycle and will
    eventually own the AnimeTitle and MangaTitle branches associated with it.

    During this foundation checkpoint, the entity contains only its canonical
    title and the slug derived from that title.
    """

    title: CanonicalTitle
    slug: Slug = field(init=False)

    def __post_init__(self) -> None:
        """Validate the entity and derive its slug."""

        if not isinstance(self.title, CanonicalTitle):
            raise ValidationError(
                "Series title must be a CanonicalTitle."
            )

        self.slug = Slug(self.title.value)

    def __str__(self) -> str:
        """Return the canonical title of the series."""
        return str(self.title)