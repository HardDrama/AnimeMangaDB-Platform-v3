"""
Domain entity representing a relationship between
one Episode and one Chapter.
"""

from dataclasses import dataclass

from animemangadb.domain.entities.chapter import Chapter
from animemangadb.domain.entities.episode import Episode
from animemangadb.domain.exceptions import ValidationError


@dataclass(eq=False)
class EpisodeChapterMapping:
    """
    Represents exactly one Episode–Chapter relationship.

    Multiple mappings may reference the same Episode.

    Multiple mappings may reference the same Chapter.

    Each mapping itself is atomic and immutable.
    """

    episode: Episode
    chapter: Chapter

    def __post_init__(self) -> None:
        if not isinstance(self.episode, Episode):
            raise ValidationError(
                "EpisodeChapterMapping episode must be an Episode."
            )

        if not isinstance(self.chapter, Chapter):
            raise ValidationError(
                "EpisodeChapterMapping chapter must be a Chapter."
            )

    def __str__(self) -> str:
        return (
            f"{self.episode.identifier} ↔ "
            f"{self.chapter.identifier}"
        )