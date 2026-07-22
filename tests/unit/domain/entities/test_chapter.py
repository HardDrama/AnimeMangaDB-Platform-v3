import pytest

from animemangadb.domain.entities import (
    Chapter,
    MangaTitle,
    Series,
)
from animemangadb.domain.exceptions import ValidationError
from animemangadb.domain.value_objects.canonical_title import (
    CanonicalTitle,
)
from animemangadb.domain.value_objects.installment_identifier import (
    InstallmentIdentifier,
)
from animemangadb.domain.value_objects.slug import Slug


def build_manga_title() -> MangaTitle:
    series = Series(
        title=CanonicalTitle("One Piece"),
    )

    return MangaTitle(
        series=series,
        title=CanonicalTitle("One Piece"),
    )


def test_chapter_accepts_valid_inputs():
    manga = build_manga_title()

    chapter = Chapter(
        manga_title=manga,
        identifier=InstallmentIdentifier("1096"),
        title=CanonicalTitle("Kumachi"),
    )

    assert chapter.manga_title is manga
    assert chapter.identifier == InstallmentIdentifier("1096")
    assert chapter.title == CanonicalTitle("Kumachi")


def test_chapter_generates_slug():
    chapter = Chapter(
        manga_title=build_manga_title(),
        identifier=InstallmentIdentifier("1096"),
        title=CanonicalTitle("Kumachi"),
    )

    assert chapter.slug == Slug("Kumachi")


def test_chapter_rejects_invalid_manga_title():
    with pytest.raises(ValidationError):
        Chapter(
            manga_title=None,  # type: ignore[arg-type]
            identifier=InstallmentIdentifier("1"),
            title=CanonicalTitle("Pilot"),
        )


def test_chapter_rejects_invalid_identifier():
    with pytest.raises(ValidationError):
        Chapter(
            manga_title=build_manga_title(),
            identifier=None,  # type: ignore[arg-type]
            title=CanonicalTitle("Pilot"),
        )


def test_chapter_rejects_invalid_title():
    with pytest.raises(ValidationError):
        Chapter(
            manga_title=build_manga_title(),
            identifier=InstallmentIdentifier("1"),
            title=None,  # type: ignore[arg-type]
        )


def test_chapter_string_representation():
    chapter = Chapter(
        manga_title=build_manga_title(),
        identifier=InstallmentIdentifier("1096"),
        title=CanonicalTitle("Kumachi"),
    )

    assert (
        str(chapter)
        == "Chapter 1096: Kumachi"
    )


def test_chapter_instances_are_not_structurally_equal():
    manga = build_manga_title()

    first = Chapter(
        manga_title=manga,
        identifier=InstallmentIdentifier("1"),
        title=CanonicalTitle("Pilot"),
    )

    second = Chapter(
        manga_title=manga,
        identifier=InstallmentIdentifier("1"),
        title=CanonicalTitle("Pilot"),
    )

    assert first is not second
    assert first != second