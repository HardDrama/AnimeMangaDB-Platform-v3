"""Tests for Platform v3 ORM persistence models."""

from sqlalchemy import UniqueConstraint, create_engine
from sqlalchemy.orm import configure_mappers

from animemangadb.infrastructure.database import (
    AnimeTitleORM,
    Base,
    ChapterORM,
    EpisodeChapterMappingORM,
    EpisodeORM,
    MangaTitleORM,
    SeriesORM,
)


EXPECTED_TABLE_NAMES = {
    "series",
    "anime_titles",
    "manga_titles",
    "episodes",
    "chapters",
    "episode_chapter_mappings",
}


def unique_constraint_names(
    model: type[Base],
) -> set[str | None]:
    """Return unique-constraint names for an ORM model."""
    return {
        constraint.name
        for constraint in model.__table__.constraints
        if isinstance(
            constraint,
            UniqueConstraint,
        )
    }


def test_all_orm_models_inherit_from_base():
    models = (
        SeriesORM,
        AnimeTitleORM,
        MangaTitleORM,
        EpisodeORM,
        ChapterORM,
        EpisodeChapterMappingORM,
    )

    for model in models:
        assert issubclass(
            model,
            Base,
        )


def test_metadata_contains_expected_tables():
    assert set(Base.metadata.tables) == EXPECTED_TABLE_NAMES


def test_series_columns_match_persistence_strategy():
    assert set(
        SeriesORM.__table__.columns.keys()
    ) == {
        "id",
        "title",
        "slug",
    }

    assert (
        SeriesORM.__table__.columns.slug.unique
        is True
    )


def test_anime_and_manga_titles_reference_series():
    anime_foreign_keys = {
        foreign_key.target_fullname
        for foreign_key
        in AnimeTitleORM.__table__.foreign_keys
    }
    manga_foreign_keys = {
        foreign_key.target_fullname
        for foreign_key
        in MangaTitleORM.__table__.foreign_keys
    }

    assert anime_foreign_keys == {
        "series.id",
    }
    assert manga_foreign_keys == {
        "series.id",
    }


def test_episode_and_chapter_preserve_string_identifiers():
    episode_identifier = (
        EpisodeORM.__table__.columns.identifier
    )
    chapter_identifier = (
        ChapterORM.__table__.columns.identifier
    )

    assert episode_identifier.type.python_type is str
    assert chapter_identifier.type.python_type is str


def test_episode_and_chapter_reference_owner_titles():
    episode_foreign_keys = {
        foreign_key.target_fullname
        for foreign_key
        in EpisodeORM.__table__.foreign_keys
    }
    chapter_foreign_keys = {
        foreign_key.target_fullname
        for foreign_key
        in ChapterORM.__table__.foreign_keys
    }

    assert episode_foreign_keys == {
        "anime_titles.id",
    }
    assert chapter_foreign_keys == {
        "manga_titles.id",
    }


def test_mapping_references_episode_and_chapter():
    mapping_foreign_keys = {
        foreign_key.target_fullname
        for foreign_key
        in EpisodeChapterMappingORM.__table__.foreign_keys
    }

    assert mapping_foreign_keys == {
        "episodes.id",
        "chapters.id",
    }


def test_scoped_uniqueness_constraints_are_defined():
    assert (
        "uq_anime_titles_series_slug"
        in unique_constraint_names(AnimeTitleORM)
    )
    assert (
        "uq_manga_titles_series_slug"
        in unique_constraint_names(MangaTitleORM)
    )
    assert (
        "uq_episodes_anime_title_identifier"
        in unique_constraint_names(EpisodeORM)
    )
    assert (
        "uq_chapters_manga_title_identifier"
        in unique_constraint_names(ChapterORM)
    )


def test_mapping_pair_has_unique_constraint():
    expected_name = (
        "uq_episode_chapter_mappings_"
        "episode_chapter"
    )

    assert expected_name in unique_constraint_names(
        EpisodeChapterMappingORM
    )


def test_all_foreign_key_columns_are_required():
    foreign_key_columns = (
        AnimeTitleORM.__table__.columns.series_id,
        MangaTitleORM.__table__.columns.series_id,
        EpisodeORM.__table__.columns.anime_title_id,
        ChapterORM.__table__.columns.manga_title_id,
        EpisodeChapterMappingORM.__table__.columns.episode_id,
        EpisodeChapterMappingORM.__table__.columns.chapter_id,
    )

    for column in foreign_key_columns:
        assert column.nullable is False


def test_relationship_mappers_configure_successfully():
    configure_mappers()


def test_metadata_can_create_and_drop_all_tables():
    engine = create_engine(
        "sqlite+pysqlite:///:memory:"
    )

    Base.metadata.create_all(engine)

    assert set(
        Base.metadata.tables
    ) == EXPECTED_TABLE_NAMES

    Base.metadata.drop_all(engine)
    engine.dispose()