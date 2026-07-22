import pytest

from animemangadb.domain.entities import Series
from animemangadb.domain.exceptions import ValidationError
from animemangadb.domain.value_objects.canonical_title import (
    CanonicalTitle,
)
from animemangadb.domain.value_objects.slug import Slug


def test_series_accepts_canonical_title():
    title = CanonicalTitle("One Piece")

    series = Series(title=title)

    assert series.title is title


def test_series_derives_slug_from_title():
    series = Series(
        title=CanonicalTitle("One Piece"),
    )

    assert series.slug == Slug("one-piece")


def test_series_derives_slug_from_title_with_punctuation():
    series = Series(
        title=CanonicalTitle(
            "Frieren: Beyond Journey's End"
        ),
    )

    assert (
        series.slug.value
        == "frieren-beyond-journeys-end"
    )


def test_series_preserves_canonical_title():
    series = Series(
        title=CanonicalTitle("BLEACH"),
    )

    assert series.title.value == "BLEACH"


def test_series_rejects_plain_string_title():
    with pytest.raises(
        ValidationError,
        match="Series title must be a CanonicalTitle.",
    ):
        Series(
            title="One Piece",  # type: ignore[arg-type]
        )


def test_series_rejects_none_title():
    with pytest.raises(
        ValidationError,
        match="Series title must be a CanonicalTitle.",
    ):
        Series(
            title=None,  # type: ignore[arg-type]
        )


def test_series_string_representation():
    series = Series(
        title=CanonicalTitle("One Piece"),
    )

    assert str(series) == "One Piece"


def test_series_instances_do_not_use_structural_equality():
    first = Series(
        title=CanonicalTitle("One Piece"),
    )
    second = Series(
        title=CanonicalTitle("One Piece"),
    )

    assert first is not second
    assert first != second