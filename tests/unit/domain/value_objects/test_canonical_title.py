import pytest

from animemangadb.domain.exceptions import ValidationError
from animemangadb.domain.value_objects.canonical_title import (
    CanonicalTitle,
)


def test_valid_title():
    title = CanonicalTitle("One Piece")

    assert title.value == "One Piece"


def test_title_is_trimmed():
    title = CanonicalTitle("  Naruto  ")

    assert title.value == "Naruto"


def test_title_preserves_case():
    title = CanonicalTitle("BLEACH")

    assert title.value == "BLEACH"


def test_title_preserves_punctuation():
    title = CanonicalTitle("Frieren: Beyond Journey's End")

    assert (
        title.value
        == "Frieren: Beyond Journey's End"
    )


def test_empty_title():
    with pytest.raises(ValidationError):
        CanonicalTitle("")


def test_whitespace_title():
    with pytest.raises(ValidationError):
        CanonicalTitle("     ")


def test_none_title():
    with pytest.raises(ValidationError):
        CanonicalTitle(None)  # type: ignore[arg-type]


def test_title_equality():
    assert (
        CanonicalTitle("One Piece")
        == CanonicalTitle("One Piece")
    )


def test_title_hashable():
    titles = {
        CanonicalTitle("One Piece"),
        CanonicalTitle("Naruto"),
    }

    assert CanonicalTitle("Naruto") in titles


def test_string_representation():
    title = CanonicalTitle("One Piece")

    assert str(title) == "One Piece"