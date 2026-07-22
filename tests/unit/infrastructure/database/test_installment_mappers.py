"""Tests for installment-level entity mappers."""

import pytest
from sqlalchemy import inspect as sqlalchemy_inspect

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
from animemangadb.infrastructure.database.mappers import (
    ChapterMapper,
    EpisodeChapterMappingMapper,
    EpisodeMapper,
    Mapper,
)
from animemangadb.infrastructure.database.models import (
    AnimeTitleORM,
    ChapterORM,
    EpisodeChapterMappingORM,
    EpisodeORM,
    MangaTitleORM,
)


def make_series() -> Series:
    return Series(
        title=CanonicalTitle("One Piece"),
    )


def make_anime_title() -> AnimeTitle:
    return AnimeTitle(
        series=make_series(),
        title=CanonicalTitle("One Piece"),
    )


def make_manga_title() -> MangaTitle:
    return MangaTitle(
        series=make_series(),
        title=CanonicalTitle("One Piece"),
    )


def make_episode() -> Episode:
    return Episode(
        anime_title=make_anime_title(),
        identifier=InstallmentIdentifier("1130"),
        title=CanonicalTitle("A History Erased"),
    )


def make_chapter() -> Chapter:
    return Chapter(
        manga_title=make_manga_title(),
        identifier=InstallmentIdentifier("1096"),
        title=CanonicalTitle("Kumachi"),
    )


def test_installment_mappers_inherit_from_mapper():
    assert issubclass(EpisodeMapper, Mapper)
    assert issubclass(ChapterMapper, Mapper)
    assert issubclass(
        EpisodeChapterMappingMapper,
        Mapper,
    )


def test_episode_to_orm_maps_scalar_fields_and_parent():
    domain_object = make_episode()
    anime_title_orm = AnimeTitleORM(
        title="One Piece",
        slug="one-piece",
    )

    orm_object = EpisodeMapper.to_orm(
        domain_object,
        anime_title_orm=anime_title_orm,
    )

    assert isinstance(orm_object, EpisodeORM)
    assert orm_object.anime_title is anime_title_orm
    assert orm_object.identifier == "1130"
    assert orm_object.title == "A History Erased"
    assert orm_object.slug == "a-history-erased"
    assert orm_object.chapter_mappings == []


def test_episode_to_domain_reconstructs_value_objects():
    anime_title = make_anime_title()
    orm_object = EpisodeORM(
        identifier="1130",
        title="A History Erased",
        slug="a-history-erased",
    )

    domain_object = EpisodeMapper.to_domain(
        orm_object,
        anime_title=anime_title,
    )

    assert isinstance(domain_object, Episode)
    assert domain_object.anime_title is anime_title
    assert isinstance(
        domain_object.identifier,
        InstallmentIdentifier,
    )
    assert domain_object.identifier.value == "1130"
    assert isinstance(
        domain_object.title,
        CanonicalTitle,
    )
    assert domain_object.title.value == "A History Erased"
    assert domain_object.slug.value == "a-history-erased"


def test_episode_round_trip_preserves_domain_state():
    original = make_episode()
    anime_title_orm = AnimeTitleORM(
        title="One Piece",
        slug="one-piece",
    )

    restored = EpisodeMapper.to_domain(
        EpisodeMapper.to_orm(
            original,
            anime_title_orm=anime_title_orm,
        ),
        anime_title=original.anime_title,
    )

    assert restored is not original
    assert restored.anime_title is original.anime_title
    assert restored.identifier == original.identifier
    assert restored.title == original.title
    assert restored.slug == original.slug


def test_episode_mapper_preserves_non_numeric_identifier():
    anime_title = make_anime_title()
    orm_object = EpisodeORM(
        identifier="OVA-2",
        title="Special Adventure",
        slug="special-adventure",
    )

    domain_object = EpisodeMapper.to_domain(
        orm_object,
        anime_title=anime_title,
    )

    assert domain_object.identifier.value == "OVA-2"


def test_episode_to_domain_rejects_inconsistent_slug():
    orm_object = EpisodeORM(
        identifier="1130",
        title="A History Erased",
        slug="incorrect-slug",
    )

    with pytest.raises(ValidationError):
        EpisodeMapper.to_domain(
            orm_object,
            anime_title=make_anime_title(),
        )


def test_episode_to_orm_is_new_and_unattached():
    anime_title_orm = AnimeTitleORM(
        title="One Piece",
        slug="one-piece",
    )

    first = EpisodeMapper.to_orm(
        make_episode(),
        anime_title_orm=anime_title_orm,
    )
    second = EpisodeMapper.to_orm(
        make_episode(),
        anime_title_orm=anime_title_orm,
    )

    assert first is not second
    assert sqlalchemy_inspect(first).session is None
    assert sqlalchemy_inspect(second).session is None
    assert "id" not in first.__dict__


def test_chapter_to_orm_maps_scalar_fields_and_parent():
    domain_object = make_chapter()
    manga_title_orm = MangaTitleORM(
        title="One Piece",
        slug="one-piece",
    )

    orm_object = ChapterMapper.to_orm(
        domain_object,
        manga_title_orm=manga_title_orm,
    )

    assert isinstance(orm_object, ChapterORM)
    assert orm_object.manga_title is manga_title_orm
    assert orm_object.identifier == "1096"
    assert orm_object.title == "Kumachi"
    assert orm_object.slug == "kumachi"
    assert orm_object.episode_mappings == []


def test_chapter_to_domain_reconstructs_value_objects():
    manga_title = make_manga_title()
    orm_object = ChapterORM(
        identifier="1096",
        title="Kumachi",
        slug="kumachi",
    )

    domain_object = ChapterMapper.to_domain(
        orm_object,
        manga_title=manga_title,
    )

    assert isinstance(domain_object, Chapter)
    assert domain_object.manga_title is manga_title
    assert isinstance(
        domain_object.identifier,
        InstallmentIdentifier,
    )
    assert domain_object.identifier.value == "1096"
    assert isinstance(
        domain_object.title,
        CanonicalTitle,
    )
    assert domain_object.title.value == "Kumachi"
    assert domain_object.slug.value == "kumachi"


def test_chapter_round_trip_preserves_domain_state():
    original = make_chapter()
    manga_title_orm = MangaTitleORM(
        title="One Piece",
        slug="one-piece",
    )

    restored = ChapterMapper.to_domain(
        ChapterMapper.to_orm(
            original,
            manga_title_orm=manga_title_orm,
        ),
        manga_title=original.manga_title,
    )

    assert restored is not original
    assert restored.manga_title is original.manga_title
    assert restored.identifier == original.identifier
    assert restored.title == original.title
    assert restored.slug == original.slug


def test_chapter_mapper_preserves_fractional_identifier():
    manga_title = make_manga_title()
    orm_object = ChapterORM(
        identifier="12.5",
        title="Interlude",
        slug="interlude",
    )

    domain_object = ChapterMapper.to_domain(
        orm_object,
        manga_title=manga_title,
    )

    assert domain_object.identifier.value == "12.5"


def test_chapter_to_domain_rejects_inconsistent_slug():
    orm_object = ChapterORM(
        identifier="1096",
        title="Kumachi",
        slug="incorrect-slug",
    )

    with pytest.raises(ValidationError):
        ChapterMapper.to_domain(
            orm_object,
            manga_title=make_manga_title(),
        )


def test_chapter_to_orm_is_new_and_unattached():
    manga_title_orm = MangaTitleORM(
        title="One Piece",
        slug="one-piece",
    )

    first = ChapterMapper.to_orm(
        make_chapter(),
        manga_title_orm=manga_title_orm,
    )
    second = ChapterMapper.to_orm(
        make_chapter(),
        manga_title_orm=manga_title_orm,
    )

    assert first is not second
    assert sqlalchemy_inspect(first).session is None
    assert sqlalchemy_inspect(second).session is None
    assert "id" not in first.__dict__


def test_mapping_to_orm_uses_resolved_relationships():
    episode = make_episode()
    chapter = make_chapter()
    domain_object = EpisodeChapterMapping(
        episode=episode,
        chapter=chapter,
    )
    episode_orm = EpisodeORM(
        identifier="1130",
        title="A History Erased",
        slug="a-history-erased",
    )
    chapter_orm = ChapterORM(
        identifier="1096",
        title="Kumachi",
        slug="kumachi",
    )

    orm_object = EpisodeChapterMappingMapper.to_orm(
        domain_object,
        episode_orm=episode_orm,
        chapter_orm=chapter_orm,
    )

    assert isinstance(
        orm_object,
        EpisodeChapterMappingORM,
    )
    assert orm_object.episode is episode_orm
    assert orm_object.chapter is chapter_orm
    assert sqlalchemy_inspect(orm_object).session is None
    assert "id" not in orm_object.__dict__


def test_mapping_to_domain_uses_resolved_entities():
    episode = make_episode()
    chapter = make_chapter()
    orm_object = EpisodeChapterMappingORM()

    domain_object = EpisodeChapterMappingMapper.to_domain(
        orm_object,
        episode=episode,
        chapter=chapter,
    )

    assert isinstance(
        domain_object,
        EpisodeChapterMapping,
    )
    assert domain_object.episode is episode
    assert domain_object.chapter is chapter


def test_mapping_round_trip_preserves_relationship_state():
    episode = make_episode()
    chapter = make_chapter()
    original = EpisodeChapterMapping(
        episode=episode,
        chapter=chapter,
    )
    episode_orm = EpisodeORM(
        identifier="1130",
        title="A History Erased",
        slug="a-history-erased",
    )
    chapter_orm = ChapterORM(
        identifier="1096",
        title="Kumachi",
        slug="kumachi",
    )

    restored = EpisodeChapterMappingMapper.to_domain(
        EpisodeChapterMappingMapper.to_orm(
            original,
            episode_orm=episode_orm,
            chapter_orm=chapter_orm,
        ),
        episode=episode,
        chapter=chapter,
    )

    assert restored is not original
    assert restored.episode is episode
    assert restored.chapter is chapter


def test_installment_mappers_do_not_mutate_inputs():
    episode = make_episode()
    chapter = make_chapter()
    episode_identifier = episode.identifier
    chapter_identifier = chapter.identifier
    anime_title_orm = AnimeTitleORM(
        title="One Piece",
        slug="one-piece",
    )
    manga_title_orm = MangaTitleORM(
        title="One Piece",
        slug="one-piece",
    )

    EpisodeMapper.to_orm(
        episode,
        anime_title_orm=anime_title_orm,
    )
    ChapterMapper.to_orm(
        chapter,
        manga_title_orm=manga_title_orm,
    )

    assert episode.identifier is episode_identifier
    assert chapter.identifier is chapter_identifier


def test_episode_mapper_rejects_wrong_types():
    with pytest.raises(TypeError):
        EpisodeMapper.to_orm(
            "episode",
            anime_title_orm=AnimeTitleORM(),
        )

    with pytest.raises(TypeError):
        EpisodeMapper.to_domain(
            "episode",
            anime_title=make_anime_title(),
        )


def test_chapter_mapper_rejects_wrong_types():
    with pytest.raises(TypeError):
        ChapterMapper.to_orm(
            "chapter",
            manga_title_orm=MangaTitleORM(),
        )

    with pytest.raises(TypeError):
        ChapterMapper.to_domain(
            "chapter",
            manga_title=make_manga_title(),
        )


def test_mapping_mapper_rejects_wrong_types():
    with pytest.raises(TypeError):
        EpisodeChapterMappingMapper.to_domain(
            "mapping",
            episode=make_episode(),
            chapter=make_chapter(),
        )

    with pytest.raises(TypeError):
        EpisodeChapterMappingMapper.to_orm(
            "mapping",
            episode_orm=EpisodeORM(),
            chapter_orm=ChapterORM(),
        )
