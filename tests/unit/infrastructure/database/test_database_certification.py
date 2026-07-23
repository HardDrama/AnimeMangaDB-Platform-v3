"""
Database Certification Tests

Platform Checkpoint
v0.5.10
"""

from collections.abc import Iterator

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from animemangadb.domain.entities import (
    AnimeTitle,
    Chapter,
    Episode,
    EpisodeChapterMapping,
    MangaTitle,
    Series,
)
from animemangadb.domain.value_objects.canonical_title import CanonicalTitle
from animemangadb.domain.value_objects.installment_identifier import (
    InstallmentIdentifier,
)
from animemangadb.infrastructure.database.base import Base
from animemangadb.infrastructure.database.repositories import (
    AnimeTitleRepository,
    ChapterRepository,
    EpisodeChapterMappingRepository,
    EpisodeRepository,
    MangaTitleRepository,
    SeriesRepository,
)

EXPECTED_TABLE_NAMES = {
    "series",
    "anime_titles",
    "manga_titles",
    "episodes",
    "chapters",
    "episode_chapter_mappings",
}


@pytest.fixture
def session() -> Iterator[Session]:
    engine = create_engine("sqlite+pysqlite:///:memory:")
    Base.metadata.create_all(engine)
    factory = sessionmaker(bind=engine, expire_on_commit=False)
    with factory() as current_session:
        yield current_session
    Base.metadata.drop_all(engine)
    engine.dispose()


def test_database_schema_contains_expected_tables():
    assert set(Base.metadata.tables) == EXPECTED_TABLE_NAMES


def test_every_repository_can_be_constructed(session: Session):
    repositories = [
        SeriesRepository(session),
        AnimeTitleRepository(session),
        MangaTitleRepository(session),
        EpisodeRepository(session),
        ChapterRepository(session),
        EpisodeChapterMappingRepository(session),
    ]
    assert len(repositories) == 6


def test_every_repository_uses_same_session(session: Session):
    repositories = [
        SeriesRepository(session),
        AnimeTitleRepository(session),
        MangaTitleRepository(session),
        EpisodeRepository(session),
        ChapterRepository(session),
        EpisodeChapterMappingRepository(session),
    ]
    assert all(r._session is session for r in repositories)


def test_repository_add_stages_without_implicit_commit(session: Session):
    repository = SeriesRepository(session)
    series = Series(CanonicalTitle("One Piece"))
    returned = repository.add(series)
    assert returned is series
    assert session.new
    assert session.in_transaction()


def test_caller_rollback_discards_repository_work(session: Session):
    repository = SeriesRepository(session)
    series = Series(CanonicalTitle("One Piece"))
    repository.add(series)
    session.rollback()
    assert repository.get_by_slug(series.slug) is None
    assert repository.list_all() == []


def test_caller_commit_persists_repository_work(session: Session):
    repository = SeriesRepository(session)
    series = Series(CanonicalTitle("One Piece"))
    repository.add(series)
    session.commit()
    restored = repository.get_by_slug(series.slug)
    assert restored is not None
    assert restored.title == series.title
    assert restored.slug == series.slug


def test_commit_survives_new_session():
    engine = create_engine("sqlite+pysqlite:///:memory:")
    Base.metadata.create_all(engine)
    factory = sessionmaker(bind=engine, expire_on_commit=False)
    series = Series(CanonicalTitle("One Piece"))
    with factory() as first:
        SeriesRepository(first).add(series)
        first.commit()
    with factory() as second:
        restored = SeriesRepository(second).get_by_slug(series.slug)
        assert restored is not None
        assert restored.slug == series.slug
    Base.metadata.drop_all(engine)
    engine.dispose()


def test_uncommitted_work_does_not_cross_sessions():
    engine = create_engine("sqlite+pysqlite:///:memory:")
    Base.metadata.create_all(engine)
    factory = sessionmaker(bind=engine, expire_on_commit=False)
    series = Series(CanonicalTitle("One Piece"))
    with factory() as first:
        SeriesRepository(first).add(series)
        with factory() as second:
            assert SeriesRepository(second).get_by_slug(series.slug) is None
    Base.metadata.drop_all(engine)
    engine.dispose()

# ============================================================
# Repository API Certification
# ============================================================


def test_get_by_title_returns_persisted_series(
    session: Session,
):
    """
    Certification Gate

    A persisted Series should be retrievable
    by its canonical title.
    """

    repository = SeriesRepository(session)

    series = Series(
        CanonicalTitle("One Piece"),
    )

    repository.add(series)
    session.commit()

    restored = repository.get_by_title(
        CanonicalTitle("One Piece"),
    )

    assert restored is not None
    assert restored.title == series.title
    assert restored.slug == series.slug


def test_exists_by_slug_returns_true_after_commit(
    session: Session,
):
    """
    Certification Gate

    exists_by_slug() should report persisted
    entities.
    """

    repository = SeriesRepository(session)

    series = Series(
        CanonicalTitle("One Piece"),
    )

    repository.add(series)
    session.commit()

    assert repository.exists_by_slug(
        series.slug,
    )


def test_delete_removes_series(
    session: Session,
):
    """
    Certification Gate

    delete() should remove a persisted Series.
    """

    repository = SeriesRepository(session)

    series = Series(
        CanonicalTitle("One Piece"),
    )

    repository.add(series)
    session.commit()

    assert repository.delete(series)

    session.commit()

    assert repository.get_by_slug(
        series.slug,
    ) is None


def test_delete_returns_false_for_missing_series(
    session: Session,
):
    """
    Certification Gate

    delete() should return False when the
    entity is not present.
    """

    repository = SeriesRepository(session)

    series = Series(
        CanonicalTitle("One Piece"),
    )

    assert repository.delete(series) is False


# ============================================================
# Domain Graph Reconstruction Certification
# ============================================================


def build_certification_graph() -> tuple[
    Series,
    AnimeTitle,
    MangaTitle,
    Episode,
    Chapter,
    EpisodeChapterMapping,
]:
    """
    Build one complete domain graph for database certification.
    """

    series = Series(
        CanonicalTitle("One Piece"),
    )
    anime_title = AnimeTitle(
        series,
        CanonicalTitle("One Piece Anime"),
    )
    manga_title = MangaTitle(
        series,
        CanonicalTitle("One Piece Manga"),
    )
    episode = Episode(
        anime_title,
        InstallmentIdentifier("1"),
        CanonicalTitle("I'm Luffy!"),
    )
    chapter = Chapter(
        manga_title,
        InstallmentIdentifier("1"),
        CanonicalTitle("Romance Dawn"),
    )
    mapping = EpisodeChapterMapping(
        episode,
        chapter,
    )

    return (
        series,
        anime_title,
        manga_title,
        episode,
        chapter,
        mapping,
    )


def stage_certification_graph(
    session: Session,
) -> tuple[
    Series,
    AnimeTitle,
    MangaTitle,
    Episode,
    Chapter,
    EpisodeChapterMapping,
]:
    """
    Stage one complete graph using all concrete repositories.
    """

    graph = build_certification_graph()
    (
        series,
        anime_title,
        manga_title,
        episode,
        chapter,
        mapping,
    ) = graph

    SeriesRepository(session).add(series)
    session.flush()

    AnimeTitleRepository(session).add(anime_title)
    MangaTitleRepository(session).add(manga_title)
    session.flush()

    EpisodeRepository(session).add(episode)
    ChapterRepository(session).add(chapter)
    session.flush()

    EpisodeChapterMappingRepository(session).add(mapping)

    return graph


def test_complete_domain_graph_reconstructs_across_sessions():
    """
    Certification Gate

    A complete Series-to-Mapping domain graph should survive
    persistence and reconstruct through fresh repositories.
    """

    engine = create_engine("sqlite+pysqlite:///:memory:")
    Base.metadata.create_all(engine)
    factory = sessionmaker(
        bind=engine,
        expire_on_commit=False,
    )

    with factory() as first_session:
        (
            _,
            anime_title,
            manga_title,
            episode,
            chapter,
            _,
        ) = stage_certification_graph(first_session)
        first_session.commit()

    with factory() as second_session:
        restored_episode = EpisodeRepository(
            second_session
        ).get_by_identifier(
            anime_title.series.slug,
            anime_title.slug,
            episode.identifier,
        )
        restored_chapter = ChapterRepository(
            second_session
        ).get_by_identifier(
            manga_title.series.slug,
            manga_title.slug,
            chapter.identifier,
        )

        assert restored_episode is not None
        assert restored_chapter is not None

        restored_mapping = EpisodeChapterMappingRepository(
            second_session
        ).get(
            restored_episode,
            restored_chapter,
        )

        assert restored_mapping is not None
        assert restored_mapping.episode.title == episode.title
        assert restored_mapping.chapter.title == chapter.title

    Base.metadata.drop_all(engine)
    engine.dispose()


def test_reconstructed_mapping_contains_complete_parent_graph(
    session: Session,
):
    """
    Certification Gate

    Reconstructing a mapping should also reconstruct the
    Episode, Chapter, title parents, and Series parents.
    """

    (
        series,
        _,
        _,
        episode,
        chapter,
        _,
    ) = stage_certification_graph(session)
    session.commit()

    restored_mapping = EpisodeChapterMappingRepository(
        session
    ).get(
        episode,
        chapter,
    )

    assert restored_mapping is not None
    assert (
        restored_mapping.episode.anime_title.series.title
        == series.title
    )
    assert (
        restored_mapping.chapter.manga_title.series.title
        == series.title
    )


def test_reconstructed_domain_graph_hides_database_identity(
    session: Session,
):
    """
    Certification Gate

    Reconstructed domain entities should not expose ORM
    primary keys or other persistence identity.
    """

    (
        _,
        _,
        _,
        episode,
        chapter,
        _,
    ) = stage_certification_graph(session)
    session.commit()

    restored_mapping = EpisodeChapterMappingRepository(
        session
    ).get(
        episode,
        chapter,
    )

    assert restored_mapping is not None

    domain_objects = (
        restored_mapping,
        restored_mapping.episode,
        restored_mapping.episode.anime_title,
        restored_mapping.episode.anime_title.series,
        restored_mapping.chapter,
        restored_mapping.chapter.manga_title,
        restored_mapping.chapter.manga_title.series,
    )

    assert all(
        not hasattr(domain_object, "id")
        for domain_object in domain_objects
    )


# ============================================================
# Repository Round-Trip Certification
# ============================================================


def test_series_round_trip_preserves_identity(
    session: Session,
):
    """
    Certification Gate

    Persisting and reloading a Series should preserve
    all observable domain state.
    """

    repository = SeriesRepository(session)

    original = Series(
        CanonicalTitle("One Piece"),
    )

    repository.add(original)
    session.commit()

    restored = repository.get_by_slug(
        original.slug,
    )

    assert restored is not None
    assert restored.title == original.title
    assert restored.slug == original.slug
    assert restored is not original

    assert restored.title == original.title
    assert restored.slug == original.slug


def test_repository_list_all_contains_round_tripped_series(
    session: Session,
):
    """
    Certification Gate

    list_all() should return reconstructed domain
    entities rather than ORM models.
    """

    repository = SeriesRepository(session)

    first = Series(
        CanonicalTitle("One Piece"),
    )

    second = Series(
        CanonicalTitle("Naruto"),
    )

    repository.add(first)
    repository.add(second)

    session.commit()

    restored = repository.list_all()

    assert len(restored) == 2

    assert all(
        isinstance(series, Series)
        for series in restored
    )

    slugs = {
        series.slug
        for series in restored
    }

    assert first.slug in slugs
    assert second.slug in slugs


def test_multiple_repository_round_trips_are_stable(
    session: Session,
):
    """
    Certification Gate

    Repeated repository loads should continue to
    produce equivalent domain entities.
    """

    repository = SeriesRepository(session)

    original = Series(
        CanonicalTitle("One Piece"),
    )

    repository.add(original)
    session.commit()

    first_load = repository.get_by_slug(
        original.slug,
    )

    second_load = repository.get_by_slug(
        original.slug,
    )

    assert first_load is not second_load

    assert first_load.title == second_load.title
    assert first_load.slug == second_load.slug
    
    assert first_load.title == second_load.title
    assert first_load.slug == second_load.slug


def test_repository_returns_domain_objects_only(
    session: Session,
):
    """
    Certification Gate

    Infrastructure objects should never escape the
    repository boundary.
    """

    repository = SeriesRepository(session)

    series = Series(
        CanonicalTitle("One Piece"),
    )

    repository.add(series)
    session.commit()

    restored = repository.get_by_slug(
        series.slug,
    )

    assert restored.__class__.__module__.startswith(
        "animemangadb.domain"
    )