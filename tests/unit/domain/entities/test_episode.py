import pytest

from animemangadb.domain.entities import (
    AnimeTitle,
    Episode,
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


def build_anime_title() -> AnimeTitle:
    series = Series(
        title=CanonicalTitle("One Piece"),
    )

    return AnimeTitle(
        series=series,
        title=CanonicalTitle("One Piece"),
    )


def test_episode_accepts_valid_inputs():
    anime = build_anime_title()

    episode = Episode(
        anime_title=anime,
        identifier=InstallmentIdentifier("1130"),
        title=CanonicalTitle("The World We See"),
    )

    assert episode.anime_title is anime
    assert episode.identifier == InstallmentIdentifier("1130")
    assert (
        episode.title
        == CanonicalTitle("The World We See")
    )


def test_episode_generates_slug():
    episode = Episode(
        anime_title=build_anime_title(),
        identifier=InstallmentIdentifier("1130"),
        title=CanonicalTitle("The World We See"),
    )

    assert episode.slug == Slug("The World We See")


def test_episode_rejects_invalid_anime_title():
    with pytest.raises(ValidationError):
        Episode(
            anime_title=None,  # type: ignore[arg-type]
            identifier=InstallmentIdentifier("1"),
            title=CanonicalTitle("Pilot"),
        )


def test_episode_rejects_invalid_identifier():
    with pytest.raises(ValidationError):
        Episode(
            anime_title=build_anime_title(),
            identifier=None,  # type: ignore[arg-type]
            title=CanonicalTitle("Pilot"),
        )


def test_episode_rejects_invalid_title():
    with pytest.raises(ValidationError):
        Episode(
            anime_title=build_anime_title(),
            identifier=InstallmentIdentifier("1"),
            title=None,  # type: ignore[arg-type]
        )


def test_episode_string_representation():
    episode = Episode(
        anime_title=build_anime_title(),
        identifier=InstallmentIdentifier("1130"),
        title=CanonicalTitle("The World We See"),
    )

    assert (
        str(episode)
        == "Episode 1130: The World We See"
    )


def test_episode_instances_are_not_structurally_equal():
    anime = build_anime_title()

    first = Episode(
        anime_title=anime,
        identifier=InstallmentIdentifier("1"),
        title=CanonicalTitle("Pilot"),
    )

    second = Episode(
        anime_title=anime,
        identifier=InstallmentIdentifier("1"),
        title=CanonicalTitle("Pilot"),
    )

    assert first is not second
    assert first != second