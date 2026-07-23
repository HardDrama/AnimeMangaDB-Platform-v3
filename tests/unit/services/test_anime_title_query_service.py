"""
AnimeTitle Query Service Tests

Feature Checkpoint
v0.6.3
"""

from unittest.mock import Mock

from animemangadb.domain.entities import AnimeTitle, Series
from animemangadb.domain.value_objects.canonical_title import CanonicalTitle
from animemangadb.services.queries import AnimeTitleQueryService


def build_anime_title() -> AnimeTitle:
    series = Series(
        CanonicalTitle("One Piece"),
    )

    return AnimeTitle(
        series,
        CanonicalTitle("One Piece Anime"),
    )


def test_get_by_slug_delegates_to_repository():
    repository = Mock()
    service = AnimeTitleQueryService(repository)
    anime_title = build_anime_title()

    repository.get_by_slug.return_value = anime_title

    result = service.get_by_slug(
        anime_title.series.slug,
        anime_title.slug,
    )

    repository.get_by_slug.assert_called_once_with(
        anime_title.series.slug,
        anime_title.slug,
    )
    assert result is anime_title


def test_get_by_title_delegates_to_repository():
    repository = Mock()
    service = AnimeTitleQueryService(repository)
    anime_title = build_anime_title()

    repository.get_by_title.return_value = anime_title

    result = service.get_by_title(
        anime_title.series.slug,
        anime_title.title,
    )

    repository.get_by_title.assert_called_once_with(
        anime_title.series.slug,
        anime_title.title,
    )
    assert result is anime_title


def test_list_for_series_delegates_to_repository():
    repository = Mock()
    service = AnimeTitleQueryService(repository)
    anime_title = build_anime_title()

    repository.list_for_series.return_value = [
        anime_title,
    ]

    result = service.list_for_series(
        anime_title.series.slug,
    )

    repository.list_for_series.assert_called_once_with(
        anime_title.series.slug,
    )
    assert result == [anime_title]


def test_get_by_slug_returns_none_when_missing():
    repository = Mock()
    service = AnimeTitleQueryService(repository)
    anime_title = build_anime_title()

    repository.get_by_slug.return_value = None

    result = service.get_by_slug(
        anime_title.series.slug,
        anime_title.slug,
    )

    assert result is None