"""
Certification tests for the complete Platform v3 Domain Layer.
"""

import ast
from pathlib import Path

from animemangadb.domain.entities import (
    AnimeTitle,
    Chapter,
    Episode,
    EpisodeChapterMapping,
    MangaTitle,
    Series,
)
from animemangadb.domain.value_objects.canonical_title import (
    CanonicalTitle,
)
from animemangadb.domain.value_objects.installment_identifier import (
    InstallmentIdentifier,
)
from animemangadb.domain.value_objects.slug import Slug


def build_series() -> Series:
    """Create a Series used by the certification tests."""
    return Series(
        title=CanonicalTitle("One Piece"),
    )


def build_anime_title(series: Series) -> AnimeTitle:
    """Create an AnimeTitle belonging to the supplied Series."""
    return AnimeTitle(
        series=series,
        title=CanonicalTitle("One Piece"),
    )


def build_manga_title(series: Series) -> MangaTitle:
    """Create a MangaTitle belonging to the supplied Series."""
    return MangaTitle(
        series=series,
        title=CanonicalTitle("One Piece"),
    )


def build_episode(
    anime_title: AnimeTitle,
    identifier: str = "1130",
    title: str = "The World We See",
) -> Episode:
    """Create an Episode belonging to the supplied AnimeTitle."""
    return Episode(
        anime_title=anime_title,
        identifier=InstallmentIdentifier(identifier),
        title=CanonicalTitle(title),
    )


def build_chapter(
    manga_title: MangaTitle,
    identifier: str = "1096",
    title: str = "Kumachi",
) -> Chapter:
    """Create a Chapter belonging to the supplied MangaTitle."""
    return Chapter(
        manga_title=manga_title,
        identifier=InstallmentIdentifier(identifier),
        title=CanonicalTitle(title),
    )


def test_complete_domain_hierarchy_can_be_constructed():
    series = build_series()
    anime_title = build_anime_title(series)
    manga_title = build_manga_title(series)
    episode = build_episode(anime_title)
    chapter = build_chapter(manga_title)

    mapping = EpisodeChapterMapping(
        episode=episode,
        chapter=chapter,
    )

    assert anime_title.series is series
    assert manga_title.series is series
    assert episode.anime_title is anime_title
    assert chapter.manga_title is manga_title
    assert mapping.episode is episode
    assert mapping.chapter is chapter


def test_anime_and_manga_are_sibling_branches_of_one_series():
    series = build_series()

    anime_title = build_anime_title(series)
    manga_title = build_manga_title(series)

    assert anime_title.series is series
    assert manga_title.series is series
    assert anime_title is not manga_title


def test_mapping_represents_exactly_one_episode_chapter_relationship():
    series = build_series()
    episode = build_episode(build_anime_title(series))
    chapter = build_chapter(build_manga_title(series))

    mapping = EpisodeChapterMapping(
        episode=episode,
        chapter=chapter,
    )

    assert isinstance(mapping.episode, Episode)
    assert isinstance(mapping.chapter, Chapter)
    assert mapping.episode is episode
    assert mapping.chapter is chapter


def test_episode_can_participate_in_multiple_mappings():
    series = build_series()
    anime_title = build_anime_title(series)
    manga_title = build_manga_title(series)

    episode = build_episode(anime_title)

    first_chapter = build_chapter(
        manga_title=manga_title,
        identifier="1096",
        title="Kumachi",
    )
    second_chapter = build_chapter(
        manga_title=manga_title,
        identifier="1097",
        title="Ginny",
    )

    first_mapping = EpisodeChapterMapping(
        episode=episode,
        chapter=first_chapter,
    )
    second_mapping = EpisodeChapterMapping(
        episode=episode,
        chapter=second_chapter,
    )

    assert first_mapping.episode is episode
    assert second_mapping.episode is episode
    assert first_mapping.chapter is not second_mapping.chapter


def test_chapter_can_participate_in_multiple_mappings():
    series = build_series()
    anime_title = build_anime_title(series)
    manga_title = build_manga_title(series)

    first_episode = build_episode(
        anime_title=anime_title,
        identifier="1129",
        title="Kuma's Past",
    )
    second_episode = build_episode(
        anime_title=anime_title,
        identifier="1130",
        title="The World We See",
    )

    chapter = build_chapter(manga_title)

    first_mapping = EpisodeChapterMapping(
        episode=first_episode,
        chapter=chapter,
    )
    second_mapping = EpisodeChapterMapping(
        episode=second_episode,
        chapter=chapter,
    )

    assert first_mapping.chapter is chapter
    assert second_mapping.chapter is chapter
    assert first_mapping.episode is not second_mapping.episode


def test_non_integer_installment_identifiers_work_in_entities():
    series = build_series()
    anime_title = build_anime_title(series)
    manga_title = build_manga_title(series)

    special_episode = build_episode(
        anime_title=anime_title,
        identifier="SP1",
        title="Special Episode",
    )
    decimal_chapter = build_chapter(
        manga_title=manga_title,
        identifier="10.5",
        title="Bonus Chapter",
    )

    mapping = EpisodeChapterMapping(
        episode=special_episode,
        chapter=decimal_chapter,
    )

    assert mapping.episode.identifier == InstallmentIdentifier("SP1")
    assert mapping.chapter.identifier == InstallmentIdentifier("10.5")


def test_slugs_are_derived_throughout_the_domain_hierarchy():
    series = Series(
        title=CanonicalTitle(
            "Frieren: Beyond Journey's End"
        ),
    )
    anime_title = AnimeTitle(
        series=series,
        title=CanonicalTitle(
            "Frieren: Beyond Journey's End"
        ),
    )
    manga_title = MangaTitle(
        series=series,
        title=CanonicalTitle(
            "Frieren: Beyond Journey's End"
        ),
    )
    episode = Episode(
        anime_title=anime_title,
        identifier=InstallmentIdentifier("1"),
        title=CanonicalTitle("The Journey's End"),
    )
    chapter = Chapter(
        manga_title=manga_title,
        identifier=InstallmentIdentifier("1"),
        title=CanonicalTitle("The Journey's End"),
    )

    assert series.slug == Slug(
        "frieren-beyond-journeys-end"
    )
    assert anime_title.slug == Slug(
        "frieren-beyond-journeys-end"
    )
    assert manga_title.slug == Slug(
        "frieren-beyond-journeys-end"
    )
    assert episode.slug == Slug(
        "the-journeys-end"
    )
    assert chapter.slug == Slug(
        "the-journeys-end"
    )


def test_domain_layer_has_no_infrastructure_framework_imports():
    repository_root = Path(__file__).resolve().parents[3]
    domain_root = (
        repository_root
        / "src"
        / "animemangadb"
        / "domain"
    )

    forbidden_modules = {
        "fastapi",
        "pydantic",
        "sqlalchemy",
    }
    violations: list[str] = []

    for source_file in domain_root.rglob("*.py"):
        syntax_tree = ast.parse(
            source_file.read_text(encoding="utf-8"),
            filename=str(source_file),
        )

        for node in ast.walk(syntax_tree):
            imported_modules: list[str] = []

            if isinstance(node, ast.Import):
                imported_modules.extend(
                    alias.name
                    for alias in node.names
                )

            if (
                isinstance(node, ast.ImportFrom)
                and node.module is not None
            ):
                imported_modules.append(node.module)

            for imported_module in imported_modules:
                root_module = imported_module.split(".", maxsplit=1)[0]

                if root_module in forbidden_modules:
                    relative_path = source_file.relative_to(
                        repository_root
                    )
                    violations.append(
                        f"{relative_path}: {imported_module}"
                    )

    assert violations == [], (
        "The Domain Layer contains forbidden "
        f"infrastructure imports: {violations}"
    )