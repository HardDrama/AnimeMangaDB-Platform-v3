"""
Domain value object representing a canonical title.
"""

from dataclasses import dataclass

from animemangadb.domain.exceptions import ValidationError

from .base import ValueObject


@dataclass(frozen=True)
class CanonicalTitle(ValueObject):
    """
    Immutable domain value object representing a canonical title.

    A canonical title preserves capitalization and punctuation while
    ensuring that the value is valid and normalized.
    """

    value: str

    def __post_init__(self) -> None:
        """Validate and normalize the title."""

        if not isinstance(self.value, str):
            raise ValidationError(
                "Canonical title must be a string."
            )

        trimmed = self.value.strip()

        if not trimmed:
            raise ValidationError(
                "Canonical title cannot be empty."
            )

        object.__setattr__(self, "value", trimmed)

    def __str__(self) -> str:
        """Return the canonical title."""
        return self.value