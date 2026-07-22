"""Certification tests for the complete repository layer."""

from collections.abc import Iterator

import pytest
from sqlalchemy import create_engine, func, select
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
from animemangadb.domain.value_objects.installment_identifier import InstallmentIdentifier
from animemangadb.infrastructure.database.base import Base
from animemangadb.infrastructure.database.models import (
    AnimeTitleORM,
    ChapterORM,
    EpisodeChapterMappingORM,
    EpisodeORM,
    MangaTitleORM,
    SeriesORM,
)
from animemangadb.infrastructure.database.repositories import (
    AnimeTitleRepository,
    ChapterRepository,
    EpisodeChapterMappingRepository,
    EpisodeRepository,
    MangaTitleRepository,
    SeriesRepository,
)


@pytest.fixture
def session_factory() -> Iterator[sessionmaker[Session]]:
    engine = create_engine("sqlite+pysqlite:///:memory:")
    Base.metadata.create_all(engine)
    factory = sessionmaker(bind=engine, expire_on_commit=False)
    yield factory
    Base.metadata.drop_all(engine)
    engine.dispose()


def build_graph():
    series = Series(CanonicalTitle("One Piece"))
    anime = AnimeTitle(series, CanonicalTitle("One Piece Anime"))
    manga = MangaTitle(series, CanonicalTitle("One Piece Manga"))
    episode = Episode(
        anime,
        InstallmentIdentifier("1"),
        CanonicalTitle("I'm Luffy!"),
    )
    chapter = Chapter(
        manga,
        InstallmentIdentifier("1"),
        CanonicalTitle("Romance Dawn"),
    )
    mapping = EpisodeChapterMapping(episode, chapter)
    return series, anime, manga, episode, chapter, mapping


def stage_graph(session: Session):
    series, anime, manga, episode, chapter, mapping = build_graph()
    SeriesRepository(session).add(series)
    session.flush()
    AnimeTitleRepository(session).add(anime)
    MangaTitleRepository(session).add(manga)
    session.flush()
    EpisodeRepository(session).add(episode)
    ChapterRepository(session).add(chapter)
    session.flush()
    EpisodeChapterMappingRepository(session).add(mapping)
    return series, anime, manga, episode, chapter, mapping


def test_complete_graph_round_trip_across_sessions(session_factory):
    with session_factory() as session:
        graph = stage_graph(session)
        session.commit()

    _, anime, manga, episode, chapter, _ = graph
    with session_factory() as session:
        restored_episode = EpisodeRepository(session).get_by_identifier(
            anime.series.slug,
            anime.slug,
            episode.identifier,
        )
        restored_chapter = ChapterRepository(session).get_by_identifier(
            manga.series.slug,
            manga.slug,
            chapter.identifier,
        )
        assert restored_episode is not None
        assert restored_chapter is not None
        restored_mapping = EpisodeChapterMappingRepository(session).get(
            restored_episode,
            restored_chapter,
        )
        assert restored_mapping is not None
        assert restored_mapping.episode.title.value == "I'm Luffy!"
        assert restored_mapping.chapter.title.value == "Romance Dawn"


def test_repository_layer_persists_all_expected_rows(session_factory):
    with session_factory() as session:
        stage_graph(session)
        session.flush()
        models = (
            SeriesORM,
            AnimeTitleORM,
            MangaTitleORM,
            EpisodeORM,
            ChapterORM,
            EpisodeChapterMappingORM,
        )
        assert [session.scalar(select(func.count()).select_from(model)) for model in models] == [1, 1, 1, 1, 1, 1]


def test_rollback_removes_complete_staged_graph(session_factory):
    with session_factory() as session:
        stage_graph(session)
        session.rollback()
        assert SeriesRepository(session).list_all() == []
        assert session.scalar(select(func.count()).select_from(EpisodeChapterMappingORM)) == 0


def test_domain_graph_does_not_expose_persistence_identity(session_factory):
    with session_factory() as session:
        _, anime, _, episode, _, _ = stage_graph(session)
        session.commit()
    with session_factory() as session:
        restored = EpisodeRepository(session).get_by_identifier(
            anime.series.slug,
            anime.slug,
            episode.identifier,
        )
        assert restored is not None
        assert not hasattr(restored, "id")
        assert not hasattr(restored.anime_title, "id")
        assert not hasattr(restored.anime_title.series, "id")


def test_installment_identity_is_scoped_by_parent(session_factory):
    with session_factory() as session:
        series = Series(CanonicalTitle("Shared"))
        anime_a = AnimeTitle(series, CanonicalTitle("Anime A"))
        anime_b = AnimeTitle(series, CanonicalTitle("Anime B"))
        SeriesRepository(session).add(series)
        session.flush()
        AnimeTitleRepository(session).add(anime_a)
        AnimeTitleRepository(session).add(anime_b)
        session.flush()
        EpisodeRepository(session).add(Episode(anime_a, InstallmentIdentifier("1"), CanonicalTitle("A1")))
        EpisodeRepository(session).add(Episode(anime_b, InstallmentIdentifier("1"), CanonicalTitle("B1")))
        session.flush()
        assert len(EpisodeRepository(session).list_for_anime_title(series.slug, anime_a.slug)) == 1
        assert len(EpisodeRepository(session).list_for_anime_title(series.slug, anime_b.slug)) == 1


def test_mapping_lists_reconstruct_complete_domain_graphs(session_factory):
    with session_factory() as session:
        _, _, _, episode, chapter, mapping = stage_graph(session)
        session.flush()
        repo = EpisodeChapterMappingRepository(session)
        by_episode = repo.list_for_episode(episode)
        by_chapter = repo.list_for_chapter(chapter)
        assert len(by_episode) == 1
        assert len(by_chapter) == 1
        assert by_episode[0].episode.anime_title.series.title.value == "One Piece"
        assert by_chapter[0].chapter.manga_title.series.title.value == "One Piece"
        assert repo.exists(mapping.episode, mapping.chapter)


def test_all_concrete_repositories_share_one_transaction(session_factory):
    with session_factory() as session:
        series, anime, manga, episode, chapter, mapping = build_graph()
        repositories = (
            SeriesRepository(session),
            AnimeTitleRepository(session),
            MangaTitleRepository(session),
            EpisodeRepository(session),
            ChapterRepository(session),
            EpisodeChapterMappingRepository(session),
        )
        repositories[0].add(series)
        session.flush()
        repositories[1].add(anime)
        repositories[2].add(manga)
        session.flush()
        repositories[3].add(episode)
        repositories[4].add(chapter)
        session.flush()
        repositories[5].add(mapping)
        assert session.in_transaction()
        session.rollback()
        assert SeriesRepository(session).get_by_slug(series.slug) is None


def test_repository_package_exports_complete_certified_surface():
    from animemangadb.infrastructure.database import repositories

    assert repositories.__all__ == [
        "Repository",
        "SeriesRepository",
        "AnimeTitleRepository",
        "MangaTitleRepository",
        "EpisodeRepository",
        "ChapterRepository",
        "EpisodeChapterMappingRepository",
    ]
