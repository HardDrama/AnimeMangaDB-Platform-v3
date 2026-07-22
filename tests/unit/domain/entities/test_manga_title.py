import pytest

from animemangadb.domain.entities import MangaTitle, Series
from animemangadb.domain.exceptions import ValidationError
from animemangadb.domain.value_objects.canonical_title import (
    CanonicalTitle,
)
from animemangadb.domain.value_objects.slug import Slug


def test_manga_title_accepts_valid_inputs():
    series = Series(CanonicalTitle("One Piece"))

    manga = MangaTitle(
        series=series,
        title=CanonicalTitle("One Piece"),
    )

    assert manga.series is series
    assert manga.title.value == "One Piece"


def test_manga_title_generates_slug():
    series = Series(CanonicalTitle("One Piece"))

    manga = MangaTitle(
        series=series,
        title=CanonicalTitle("One Piece"),
    )

    assert manga.slug == Slug("one-piece")


def test_manga_title_rejects_invalid_series():
    with pytest.raises(ValidationError):
        MangaTitle(
            series=None,  # type: ignore[arg-type]
            title=CanonicalTitle("One Piece"),
        )


def test_manga_title_rejects_invalid_title():
    series = Series(CanonicalTitle("One Piece"))

    with pytest.raises(ValidationError):
        MangaTitle(
            series=series,
            title=None,  # type: ignore[arg-type]
        )


def test_manga_title_string_representation():
    series = Series(CanonicalTitle("One Piece"))

    manga = MangaTitle(
        series=series,
        title=CanonicalTitle("One Piece"),
    )

    assert str(manga) == "One Piece"