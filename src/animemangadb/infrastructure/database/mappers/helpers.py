"""Shared conversion helpers for database entity mappers."""

from __future__ import annotations

from animemangadb.domain.exceptions import ValidationError
from animemangadb.domain.value_objects.canonical_title import (
    CanonicalTitle,
)
from animemangadb.domain.value_objects.installment_identifier import (
    InstallmentIdentifier,
)
from animemangadb.domain.value_objects.slug import Slug


def canonical_title_to_string(value: CanonicalTitle) -> str:
    """Return the primitive string stored by the ORM layer."""
    if not isinstance(value, CanonicalTitle):
        raise TypeError(
            "value must be a CanonicalTitle."
        )

    return value.value


def canonical_title_from_string(value: str) -> CanonicalTitle:
    """Reconstruct a CanonicalTitle from persisted text."""
    return CanonicalTitle(value)


def slug_to_string(value: Slug) -> str:
    """Return the primitive string stored by the ORM layer."""
    if not isinstance(value, Slug):
        raise TypeError(
            "value must be a Slug."
        )

    return value.value


def installment_identifier_to_string(
    value: InstallmentIdentifier,
) -> str:
    """Return the primitive installment identifier."""
    if not isinstance(value, InstallmentIdentifier):
        raise TypeError(
            "value must be an InstallmentIdentifier."
        )

    return value.value


def installment_identifier_from_string(
    value: str,
) -> InstallmentIdentifier:
    """Reconstruct an installment identifier from persisted text."""
    return InstallmentIdentifier(value)


def validate_derived_slug(
    *,
    persisted_slug: str,
    derived_slug: Slug,
) -> None:
    """Verify that persisted and Domain-derived slugs agree.

    Domain entities derive their slug from their canonical title.
    A mismatch therefore indicates invalid persisted state rather
    than an alternate Domain representation.
    """
    if persisted_slug != derived_slug.value:
        raise ValidationError(
            "Persisted slug does not match the slug derived "
            "from the canonical title."
        )
