"""
MangaTitle Query Service Tests

Feature Checkpoint
v0.6.3
"""

from unittest.mock import Mock

from animemangadb.domain.entities import MangaTitle, Series
from animemangadb.domain.value_objects.canonical_title import CanonicalTitle
from animemangadb.services.queries import MangaTitleQueryService


def build_manga_title() -> MangaTitle:
    series = Series(
        CanonicalTitle("One Piece"),
    )

    return MangaTitle(
        series,
        CanonicalTitle("One Piece Manga"),
    )


def test_get_by_slug_delegates_to_repository():
    repository = Mock()
    service = MangaTitleQueryService(repository)
    manga_title = build_manga_title()

    repository.get_by_slug.return_value = manga_title

    result = service.get_by_slug(
        manga_title.series.slug,
        manga_title.slug,
    )

    repository.get_by_slug.assert_called_once_with(
        manga_title.series.slug,
        manga_title.slug,
    )
    assert result is manga_title


def test_get_by_title_delegates_to_repository():
    repository = Mock()
    service = MangaTitleQueryService(repository)
    manga_title = build_manga_title()

    repository.get_by_title.return_value = manga_title

    result = service.get_by_title(
        manga_title.series.slug,
        manga_title.title,
    )

    repository.get_by_title.assert_called_once_with(
        manga_title.series.slug,
        manga_title.title,
    )
    assert result is manga_title


def test_list_for_series_delegates_to_repository():
    repository = Mock()
    service = MangaTitleQueryService(repository)
    manga_title = build_manga_title()

    repository.list_for_series.return_value = [
        manga_title,
    ]

    result = service.list_for_series(
        manga_title.series.slug,
    )

    repository.list_for_series.assert_called_once_with(
        manga_title.series.slug,
    )
    assert result == [manga_title]


def test_get_by_slug_returns_none_when_missing():
    repository = Mock()
    service = MangaTitleQueryService(repository)
    manga_title = build_manga_title()

    repository.get_by_slug.return_value = None

    result = service.get_by_slug(
        manga_title.series.slug,
        manga_title.slug,
    )

    assert result is None