"""
Application-layer exceptions.

These exceptions describe failures in application use cases without
exposing infrastructure or transport-specific details.
"""

from __future__ import annotations

from animemangadb.domain.value_objects.slug import Slug


class ApplicationServiceError(Exception):
    """
    Base exception for application-service failures.
    """


class SeriesAlreadyExistsError(ApplicationServiceError):
    """
    Raised when Series creation conflicts with an existing slug.
    """

    def __init__(self, slug: Slug) -> None:
        self.slug = slug
        super().__init__(
            f"A Series with slug '{slug.value}' already exists."
        )
