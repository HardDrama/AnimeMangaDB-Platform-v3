import pytest

from animemangadb.domain.entities import (
    AnimeTitle,
    Chapter,
    Episode,
    EpisodeChapterMapping,
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


def build_mapping():
    series = Series(
        title=CanonicalTitle("One Piece"),
    )

    anime = AnimeTitle(
        series=series,
        title=CanonicalTitle("One Piece"),
    )

    manga = MangaTitle(
        series=series,
        title=CanonicalTitle("One Piece"),
    )

    episode = Episode(
        anime_title=anime,
        identifier=InstallmentIdentifier("1130"),
        title=CanonicalTitle("The World We See"),
    )

    chapter = Chapter(
        manga_title=manga,
        identifier=InstallmentIdentifier("1096"),
        title=CanonicalTitle("Kumachi"),
    )

    return EpisodeChapterMapping(
        episode=episode,
        chapter=chapter,
    )


def test_mapping_accepts_valid_entities():
    mapping = build_mapping()

    assert mapping.episode.identifier.value == "1130"
    assert mapping.chapter.identifier.value == "1096"


def test_mapping_rejects_invalid_episode():
    series = Series(CanonicalTitle("One Piece"))

    manga = MangaTitle(
        series=series,
        title=CanonicalTitle("One Piece"),
    )

    chapter = Chapter(
        manga_title=manga,
        identifier=InstallmentIdentifier("1096"),
        title=CanonicalTitle("Kumachi"),
    )

    with pytest.raises(ValidationError):
        EpisodeChapterMapping(
            episode=None,  # type: ignore[arg-type]
            chapter=chapter,
        )


def test_mapping_rejects_invalid_chapter():
    series = Series(CanonicalTitle("One Piece"))

    anime = AnimeTitle(
        series=series,
        title=CanonicalTitle("One Piece"),
    )

    episode = Episode(
        anime_title=anime,
        identifier=InstallmentIdentifier("1130"),
        title=CanonicalTitle("The World We See"),
    )

    with pytest.raises(ValidationError):
        EpisodeChapterMapping(
            episode=episode,
            chapter=None,  # type: ignore[arg-type]
        )


def test_mapping_string_representation():
    mapping = build_mapping()

    assert str(mapping) == "1130 ↔ 1096"


def test_mapping_entities_are_not_structurally_equal():
    first = build_mapping()
    second = build_mapping()

    assert first is not second
    assert first != second