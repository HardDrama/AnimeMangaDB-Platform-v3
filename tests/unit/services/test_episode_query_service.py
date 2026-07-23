"""
Episode Query Service Tests

Feature Checkpoint
v0.6.4
"""

from unittest.mock import Mock

from animemangadb.domain.entities import AnimeTitle, Episode, Series
from animemangadb.domain.value_objects.canonical_title import CanonicalTitle
from animemangadb.domain.value_objects.installment_identifier import (
    InstallmentIdentifier,
)
from animemangadb.services.queries import EpisodeQueryService


def build_episode() -> Episode:
    series = Series(
        CanonicalTitle("One Piece"),
    )
    anime_title = AnimeTitle(
        series,
        CanonicalTitle("One Piece Anime"),
    )

    return Episode(
        anime_title,
        InstallmentIdentifier("1"),
        CanonicalTitle("I'm Luffy!"),
    )


def test_get_by_identifier_delegates_to_repository():
    repository = Mock()
    service = EpisodeQueryService(repository)
    episode = build_episode()

    repository.get_by_identifier.return_value = episode

    result = service.get_by_identifier(
        episode.anime_title.series.slug,
        episode.anime_title.slug,
        episode.identifier,
    )

    repository.get_by_identifier.assert_called_once_with(
        episode.anime_title.series.slug,
        episode.anime_title.slug,
        episode.identifier,
    )
    assert result is episode


def test_list_for_anime_title_delegates_to_repository():
    repository = Mock()
    service = EpisodeQueryService(repository)
    episode = build_episode()

    repository.list_for_anime_title.return_value = [
        episode,
    ]

    result = service.list_for_anime_title(
        episode.anime_title.series.slug,
        episode.anime_title.slug,
    )

    repository.list_for_anime_title.assert_called_once_with(
        episode.anime_title.series.slug,
        episode.anime_title.slug,
    )
    assert result == [episode]


def test_get_by_identifier_returns_none_when_missing():
    repository = Mock()
    service = EpisodeQueryService(repository)
    episode = build_episode()

    repository.get_by_identifier.return_value = None

    result = service.get_by_identifier(
        episode.anime_title.series.slug,
        episode.anime_title.slug,
        episode.identifier,
    )

    assert result is None
