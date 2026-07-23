"""
Series Query Service Tests

Feature Checkpoint
v0.6.2
"""

from unittest.mock import Mock

from animemangadb.domain.entities import Series
from animemangadb.domain.value_objects.canonical_title import CanonicalTitle
from animemangadb.services.queries import (
    SeriesQueryService,
)


def test_query_service_delegates_to_repository():
    repository = Mock()

    service = SeriesQueryService(repository)

    slug = Series(
        CanonicalTitle("One Piece"),
    ).slug

    expected = Series(
        CanonicalTitle("One Piece"),
    )

    repository.get_by_slug.return_value = expected

    result = service.get_by_slug(slug)

    repository.get_by_slug.assert_called_once_with(slug)

    assert result is expected


def test_query_service_returns_none_when_missing():
    repository = Mock()

    repository.get_by_slug.return_value = None

    service = SeriesQueryService(repository)

    slug = Series(
        CanonicalTitle("Missing"),
    ).slug

    assert service.get_by_slug(slug) is None