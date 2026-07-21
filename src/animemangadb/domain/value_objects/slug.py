"""
Domain value object representing a slug.
"""

from dataclasses import dataclass
import re

from animemangadb.domain.exceptions import ValidationError

from .base import ValueObject


def _normalize_slug(value: str) -> str:
    """
    Normalize a string into a URL-friendly slug.
    """

    normalized = value.strip().lower()

    # Replace whitespace with hyphens.
    normalized = re.sub(r"\s+", "-", normalized)

    # Remove characters that are not letters, numbers, or hyphens.
    normalized = re.sub(r"[^a-z0-9-]", "", normalized)

    # Collapse repeated hyphens.
    normalized = re.sub(r"-+", "-", normalized)

    # Remove leading/trailing hyphens.
    normalized = normalized.strip("-")

    return normalized


@dataclass(frozen=True)
class Slug(ValueObject):
    """
    Immutable domain value object representing a slug.
    """

    value: str

    def __post_init__(self) -> None:
        if not isinstance(self.value, str):
            raise ValidationError(
                "Slug must be a string."
            )

        normalized = _normalize_slug(self.value)

        if not normalized:
            raise ValidationError(
                "Slug cannot be empty."
            )

        object.__setattr__(self, "value", normalized)

    def __str__(self) -> str:
        return self.value