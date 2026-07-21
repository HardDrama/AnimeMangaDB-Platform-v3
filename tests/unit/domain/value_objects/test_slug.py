import pytest

from animemangadb.domain.exceptions import ValidationError
from animemangadb.domain.value_objects.slug import Slug


def test_basic_slug():
    assert Slug("One Piece").value == "one-piece"


def test_slug_lowercase():
    assert Slug("BLEACH").value == "bleach"


def test_slug_trims_whitespace():
    assert Slug("  Naruto  ").value == "naruto"


def test_slug_removes_punctuation():
    assert (
        Slug("Frieren: Beyond Journey's End").value
        == "frieren-beyond-journeys-end"
    )


def test_slug_collapses_multiple_spaces():
    assert (
        Slug("The     Apothecary     Diaries").value
        == "the-apothecary-diaries"
    )


def test_slug_collapses_multiple_hyphens():
    assert Slug("One---Piece").value == "one-piece"


def test_empty_slug():
    with pytest.raises(ValidationError):
        Slug("")


def test_whitespace_slug():
    with pytest.raises(ValidationError):
        Slug("     ")


def test_none_slug():
    with pytest.raises(ValidationError):
        Slug(None)  # type: ignore[arg-type]


def test_slug_equality():
    assert Slug("One Piece") == Slug("one-piece")


def test_slug_hashable():
    slugs = {
        Slug("One Piece"),
        Slug("Naruto"),
    }

    assert Slug("One Piece") in slugs


def test_string_representation():
    assert str(Slug("One Piece")) == "one-piece"