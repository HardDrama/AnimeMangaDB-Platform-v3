"""
Chapter Query Service Tests

Feature Checkpoint
v0.6.4
"""

from unittest.mock import Mock

from animemangadb.domain.entities import Chapter, MangaTitle, Series
from animemangadb.domain.value_objects.canonical_title import CanonicalTitle
from animemangadb.domain.value_objects.installment_identifier import (
    InstallmentIdentifier,
)
from animemangadb.services.queries import ChapterQueryService


def build_chapter() -> Chapter:
    series = Series(
        CanonicalTitle("One Piece"),
    )
    manga_title = MangaTitle(
        series,
        CanonicalTitle("One Piece Manga"),
    )

    return Chapter(
        manga_title,
        InstallmentIdentifier("1"),
        CanonicalTitle("Romance Dawn"),
    )


def test_get_by_identifier_delegates_to_repository():
    repository = Mock()
    service = ChapterQueryService(repository)
    chapter = build_chapter()

    repository.get_by_identifier.return_value = chapter

    result = service.get_by_identifier(
        chapter.manga_title.series.slug,
        chapter.manga_title.slug,
        chapter.identifier,
    )

    repository.get_by_identifier.assert_called_once_with(
        chapter.manga_title.series.slug,
        chapter.manga_title.slug,
        chapter.identifier,
    )
    assert result is chapter


def test_list_for_manga_title_delegates_to_repository():
    repository = Mock()
    service = ChapterQueryService(repository)
    chapter = build_chapter()

    repository.list_for_manga_title.return_value = [
        chapter,
    ]

    result = service.list_for_manga_title(
        chapter.manga_title.series.slug,
        chapter.manga_title.slug,
    )

    repository.list_for_manga_title.assert_called_once_with(
        chapter.manga_title.series.slug,
        chapter.manga_title.slug,
    )
    assert result == [chapter]


def test_get_by_identifier_returns_none_when_missing():
    repository = Mock()
    service = ChapterQueryService(repository)
    chapter = build_chapter()

    repository.get_by_identifier.return_value = None

    result = service.get_by_identifier(
        chapter.manga_title.series.slug,
        chapter.manga_title.slug,
        chapter.identifier,
    )

    assert result is None
