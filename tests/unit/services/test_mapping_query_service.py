"""
Episode-Chapter Mapping Query Service Tests

Feature Checkpoint
v0.6.5
"""

from unittest.mock import Mock

from animemangadb.domain.entities import (
    AnimeTitle,
    Chapter,
    Episode,
    EpisodeChapterMapping,
    MangaTitle,
    Series,
)
from animemangadb.domain.value_objects.canonical_title import CanonicalTitle
from animemangadb.domain.value_objects.installment_identifier import (
    InstallmentIdentifier,
)
from animemangadb.services.queries import (
    EpisodeChapterMappingQueryService,
)


def build_episode_and_chapter() -> tuple[Episode, Chapter]:
    series = Series(
        CanonicalTitle("One Piece"),
    )
    anime_title = AnimeTitle(
        series,
        CanonicalTitle("One Piece Anime"),
    )
    manga_title = MangaTitle(
        series,
        CanonicalTitle("One Piece Manga"),
    )
    episode = Episode(
        anime_title,
        InstallmentIdentifier("1"),
        CanonicalTitle("I'm Luffy!"),
    )
    chapter = Chapter(
        manga_title,
        InstallmentIdentifier("1"),
        CanonicalTitle("Romance Dawn"),
    )

    return episode, chapter


def test_mapping_query_service_accepts_repository():
    repository = Mock()

    service = EpisodeChapterMappingQueryService(
        repository,
    )

    assert service._repository is repository


def test_get_delegates_to_repository():
    repository = Mock()
    service = EpisodeChapterMappingQueryService(repository)
    episode, chapter = build_episode_and_chapter()
    mapping = EpisodeChapterMapping(
        episode,
        chapter,
    )

    repository.get.return_value = mapping

    result = service.get(
        episode,
        chapter,
    )

    repository.get.assert_called_once_with(
        episode,
        chapter,
    )
    assert result is mapping


def test_get_returns_none_when_mapping_is_missing():
    repository = Mock()
    service = EpisodeChapterMappingQueryService(repository)
    episode, chapter = build_episode_and_chapter()

    repository.get.return_value = None

    result = service.get(
        episode,
        chapter,
    )

    repository.get.assert_called_once_with(
        episode,
        chapter,
    )
    assert result is None


def test_list_for_episode_delegates_to_repository():
    repository = Mock()
    service = EpisodeChapterMappingQueryService(repository)
    episode, chapter = build_episode_and_chapter()
    mappings = [
        EpisodeChapterMapping(
            episode,
            chapter,
        ),
    ]

    repository.list_for_episode.return_value = mappings

    result = service.list_for_episode(
        episode,
    )

    repository.list_for_episode.assert_called_once_with(
        episode,
    )
    assert result is mappings


def test_list_for_episode_returns_empty_list_when_no_mappings_exist():
    repository = Mock()
    service = EpisodeChapterMappingQueryService(repository)
    episode, _ = build_episode_and_chapter()

    repository.list_for_episode.return_value = []

    result = service.list_for_episode(
        episode,
    )

    repository.list_for_episode.assert_called_once_with(
        episode,
    )
    assert result == []


def test_list_for_chapter_delegates_to_repository():
    repository = Mock()
    service = EpisodeChapterMappingQueryService(repository)
    episode, chapter = build_episode_and_chapter()
    mappings = [
        EpisodeChapterMapping(
            episode,
            chapter,
        ),
    ]

    repository.list_for_chapter.return_value = mappings

    result = service.list_for_chapter(
        chapter,
    )

    repository.list_for_chapter.assert_called_once_with(
        chapter,
    )
    assert result is mappings


def test_list_for_chapter_returns_empty_list_when_no_mappings_exist():
    repository = Mock()
    service = EpisodeChapterMappingQueryService(repository)
    _, chapter = build_episode_and_chapter()

    repository.list_for_chapter.return_value = []

    result = service.list_for_chapter(
        chapter,
    )

    repository.list_for_chapter.assert_called_once_with(
        chapter,
    )
    assert result == []