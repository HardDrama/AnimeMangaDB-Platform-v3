import pytest

from animemangadb.domain.entities import AnimeTitle, Series
from animemangadb.domain.exceptions import ValidationError
from animemangadb.domain.value_objects.canonical_title import (
    CanonicalTitle,
)
from animemangadb.domain.value_objects.slug import Slug


def test_anime_title_accepts_valid_inputs():
    series = Series(CanonicalTitle("One Piece"))

    anime = AnimeTitle(
        series=series,
        title=CanonicalTitle("One Piece"),
    )

    assert anime.series is series
    assert anime.title.value == "One Piece"


def test_anime_title_generates_slug():
    series = Series(CanonicalTitle("One Piece"))

    anime = AnimeTitle(
        series=series,
        title=CanonicalTitle("One Piece"),
    )

    assert anime.slug == Slug("one-piece")


def test_anime_title_rejects_invalid_series():
    with pytest.raises(ValidationError):
        AnimeTitle(
            series=None,  # type: ignore[arg-type]
            title=CanonicalTitle("One Piece"),
        )


def test_anime_title_rejects_invalid_title():
    series = Series(CanonicalTitle("One Piece"))

    with pytest.raises(ValidationError):
        AnimeTitle(
            series=series,
            title=None,  # type: ignore[arg-type]
        )


def test_anime_title_string_representation():
    series = Series(CanonicalTitle("One Piece"))

    anime = AnimeTitle(
        series=series,
        title=CanonicalTitle("One Piece"),
    )

    assert str(anime) == "One Piece"