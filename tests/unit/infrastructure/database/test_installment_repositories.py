"""Tests for installment repositories."""

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
from animemangadb.domain.value_objects.installment_identifier import InstallmentIdentifier
from animemangadb.infrastructure.database.base import Base
from animemangadb.infrastructure.database.models import (
    AnimeTitleORM,
    EpisodeChapterMappingORM,
    MangaTitleORM,
    SeriesORM,
)
from animemangadb.infrastructure.database.repositories import (
    ChapterRepository,
    EpisodeChapterMappingRepository,
    EpisodeRepository,
)


@pytest.fixture
def session() -> Iterator[Session]:
    engine = create_engine("sqlite+pysqlite:///:memory:")
    Base.metadata.create_all(engine)
    factory = sessionmaker(bind=engine, expire_on_commit=False)
    with factory() as current_session:
        yield current_session
    Base.metadata.drop_all(engine)
    engine.dispose()


@pytest.fixture
def graph(session: Session):
    series = Series(CanonicalTitle("One Piece"))
    anime = AnimeTitle(series, CanonicalTitle("One Piece Anime"))
    manga = MangaTitle(series, CanonicalTitle("One Piece Manga"))
    series_orm = SeriesORM(title=series.title.value, slug=series.slug.value)
    anime_orm = AnimeTitleORM(series=series_orm, title=anime.title.value, slug=anime.slug.value)
    manga_orm = MangaTitleORM(series=series_orm, title=manga.title.value, slug=manga.slug.value)
    session.add_all([series_orm, anime_orm, manga_orm])
    session.flush()
    return series, anime, manga


def make_episode(anime: AnimeTitle, identifier: str = "1", title: str = "Episode One") -> Episode:
    return Episode(anime, InstallmentIdentifier(identifier), CanonicalTitle(title))


def make_chapter(manga: MangaTitle, identifier: str = "1", title: str = "Chapter One") -> Chapter:
    return Chapter(manga, InstallmentIdentifier(identifier), CanonicalTitle(title))


def persist_installments(session: Session, graph):
    _, anime, manga = graph
    episode = make_episode(anime)
    chapter = make_chapter(manga)
    EpisodeRepository(session).add(episode)
    ChapterRepository(session).add(chapter)
    session.flush()
    return episode, chapter


# EpisodeRepository: 10 tests

def test_episode_add_stages_domain_entity(session, graph):
    _, anime, _ = graph
    episode = make_episode(anime)
    assert EpisodeRepository(session).add(episode) is episode
    assert len(session.new) == 1


def test_episode_add_rejects_wrong_type(session):
    with pytest.raises(TypeError):
        EpisodeRepository(session).add(object())


def test_episode_add_requires_persisted_parent(session):
    series = Series(CanonicalTitle("Missing"))
    anime = AnimeTitle(series, CanonicalTitle("Missing Anime"))
    with pytest.raises(LookupError):
        EpisodeRepository(session).add(make_episode(anime))


def test_episode_get_by_identifier_composes_graph(session, graph):
    _, anime, _ = graph
    episode = make_episode(anime)
    repo = EpisodeRepository(session)
    repo.add(episode)
    session.flush()
    restored = repo.get_by_identifier(anime.series.slug, anime.slug, episode.identifier)
    assert restored is not None
    assert restored.identifier.value == "1"
    assert restored.anime_title.title.value == "One Piece Anime"
    assert restored.anime_title.series.title.value == "One Piece"


def test_episode_get_by_identifier_returns_none(session, graph):
    _, anime, _ = graph
    result = EpisodeRepository(session).get_by_identifier(
        anime.series.slug, anime.slug, InstallmentIdentifier("999")
    )
    assert result is None


def test_episode_exists_by_identifier(session, graph):
    _, anime, _ = graph
    episode = make_episode(anime)
    repo = EpisodeRepository(session)
    repo.add(episode)
    session.flush()
    assert repo.exists_by_identifier(anime.series.slug, anime.slug, episode.identifier)


def test_episode_list_for_anime_title_uses_persistence_order(session, graph):
    _, anime, _ = graph
    repo = EpisodeRepository(session)
    repo.add(make_episode(anime, "2", "Second"))
    repo.add(make_episode(anime, "1", "First"))
    session.flush()
    assert [item.identifier.value for item in repo.list_for_anime_title(anime.series.slug, anime.slug)] == ["2", "1"]


def test_episode_delete_returns_true_and_stages_delete(session, graph):
    episode, _ = persist_installments(session, graph)
    repo = EpisodeRepository(session)
    assert repo.delete(episode)
    session.flush()
    assert repo.get_by_identifier(episode.anime_title.series.slug, episode.anime_title.slug, episode.identifier) is None


def test_episode_delete_returns_false_when_missing(session, graph):
    _, anime, _ = graph
    assert not EpisodeRepository(session).delete(make_episode(anime))


def test_episode_repository_does_not_commit(session, graph):
    _, anime, _ = graph
    repo = EpisodeRepository(session)
    repo.add(make_episode(anime))
    session.rollback()
    assert repo.list_for_anime_title(anime.series.slug, anime.slug) == []


# ChapterRepository: 10 tests

def test_chapter_add_stages_domain_entity(session, graph):
    _, _, manga = graph
    chapter = make_chapter(manga)
    assert ChapterRepository(session).add(chapter) is chapter
    assert len(session.new) == 1


def test_chapter_add_rejects_wrong_type(session):
    with pytest.raises(TypeError):
        ChapterRepository(session).add(object())


def test_chapter_add_requires_persisted_parent(session):
    series = Series(CanonicalTitle("Missing"))
    manga = MangaTitle(series, CanonicalTitle("Missing Manga"))
    with pytest.raises(LookupError):
        ChapterRepository(session).add(make_chapter(manga))


def test_chapter_get_by_identifier_composes_graph(session, graph):
    _, _, manga = graph
    chapter = make_chapter(manga)
    repo = ChapterRepository(session)
    repo.add(chapter)
    session.flush()
    restored = repo.get_by_identifier(manga.series.slug, manga.slug, chapter.identifier)
    assert restored is not None
    assert restored.identifier.value == "1"
    assert restored.manga_title.title.value == "One Piece Manga"
    assert restored.manga_title.series.title.value == "One Piece"


def test_chapter_get_by_identifier_returns_none(session, graph):
    _, _, manga = graph
    result = ChapterRepository(session).get_by_identifier(
        manga.series.slug, manga.slug, InstallmentIdentifier("999")
    )
    assert result is None


def test_chapter_exists_by_identifier(session, graph):
    _, _, manga = graph
    chapter = make_chapter(manga)
    repo = ChapterRepository(session)
    repo.add(chapter)
    session.flush()
    assert repo.exists_by_identifier(manga.series.slug, manga.slug, chapter.identifier)


def test_chapter_list_for_manga_title_uses_persistence_order(session, graph):
    _, _, manga = graph
    repo = ChapterRepository(session)
    repo.add(make_chapter(manga, "2", "Second"))
    repo.add(make_chapter(manga, "1", "First"))
    session.flush()
    assert [item.identifier.value for item in repo.list_for_manga_title(manga.series.slug, manga.slug)] == ["2", "1"]


def test_chapter_delete_returns_true_and_stages_delete(session, graph):
    _, chapter = persist_installments(session, graph)
    repo = ChapterRepository(session)
    assert repo.delete(chapter)
    session.flush()
    assert repo.get_by_identifier(chapter.manga_title.series.slug, chapter.manga_title.slug, chapter.identifier) is None


def test_chapter_delete_returns_false_when_missing(session, graph):
    _, _, manga = graph
    assert not ChapterRepository(session).delete(make_chapter(manga))


def test_chapter_repository_does_not_commit(session, graph):
    _, _, manga = graph
    repo = ChapterRepository(session)
    repo.add(make_chapter(manga))
    session.rollback()
    assert repo.list_for_manga_title(manga.series.slug, manga.slug) == []


# MappingRepository: 12 tests

def test_mapping_add_stages_domain_entity(session, graph):
    episode, chapter = persist_installments(session, graph)
    mapping = EpisodeChapterMapping(episode, chapter)
    assert EpisodeChapterMappingRepository(session).add(mapping) is mapping
    assert len(session.new) == 1


def test_mapping_add_rejects_wrong_type(session):
    with pytest.raises(TypeError):
        EpisodeChapterMappingRepository(session).add(object())


def test_mapping_add_requires_persisted_episode(session, graph):
    _, anime, manga = graph
    chapter = make_chapter(manga)
    ChapterRepository(session).add(chapter)
    session.flush()
    with pytest.raises(LookupError):
        EpisodeChapterMappingRepository(session).add(EpisodeChapterMapping(make_episode(anime), chapter))


def test_mapping_add_requires_persisted_chapter(session, graph):
    _, anime, manga = graph
    episode = make_episode(anime)
    EpisodeRepository(session).add(episode)
    session.flush()
    with pytest.raises(LookupError):
        EpisodeChapterMappingRepository(session).add(EpisodeChapterMapping(episode, make_chapter(manga)))


def test_mapping_get_composes_full_graph(session, graph):
    episode, chapter = persist_installments(session, graph)
    repo = EpisodeChapterMappingRepository(session)
    repo.add(EpisodeChapterMapping(episode, chapter))
    session.flush()
    restored = repo.get(episode, chapter)
    assert restored is not None
    assert restored.episode.anime_title.series.title.value == "One Piece"
    assert restored.chapter.manga_title.series.title.value == "One Piece"


def test_mapping_get_returns_none(session, graph):
    episode, chapter = persist_installments(session, graph)
    assert EpisodeChapterMappingRepository(session).get(episode, chapter) is None


def test_mapping_exists(session, graph):
    episode, chapter = persist_installments(session, graph)
    repo = EpisodeChapterMappingRepository(session)
    repo.add(EpisodeChapterMapping(episode, chapter))
    session.flush()
    assert repo.exists(episode, chapter)


def test_mapping_list_for_episode(session, graph):
    _, anime, manga = graph
    episode = make_episode(anime)
    chapter1 = make_chapter(manga, "1", "One")
    chapter2 = make_chapter(manga, "2", "Two")
    EpisodeRepository(session).add(episode)
    ChapterRepository(session).add(chapter1)
    ChapterRepository(session).add(chapter2)
    session.flush()
    repo = EpisodeChapterMappingRepository(session)
    repo.add(EpisodeChapterMapping(episode, chapter1))
    repo.add(EpisodeChapterMapping(episode, chapter2))
    session.flush()
    assert [m.chapter.identifier.value for m in repo.list_for_episode(episode)] == ["1", "2"]


def test_mapping_list_for_chapter(session, graph):
    _, anime, manga = graph
    episode1 = make_episode(anime, "1", "One")
    episode2 = make_episode(anime, "2", "Two")
    chapter = make_chapter(manga)
    EpisodeRepository(session).add(episode1)
    EpisodeRepository(session).add(episode2)
    ChapterRepository(session).add(chapter)
    session.flush()
    repo = EpisodeChapterMappingRepository(session)
    repo.add(EpisodeChapterMapping(episode1, chapter))
    repo.add(EpisodeChapterMapping(episode2, chapter))
    session.flush()
    assert [m.episode.identifier.value for m in repo.list_for_chapter(chapter)] == ["1", "2"]


def test_mapping_delete_returns_true(session, graph):
    episode, chapter = persist_installments(session, graph)
    mapping = EpisodeChapterMapping(episode, chapter)
    repo = EpisodeChapterMappingRepository(session)
    repo.add(mapping)
    session.flush()
    assert repo.delete(mapping)
    session.flush()
    assert not repo.exists(episode, chapter)


def test_mapping_delete_returns_false_when_missing(session, graph):
    episode, chapter = persist_installments(session, graph)
    assert not EpisodeChapterMappingRepository(session).delete(EpisodeChapterMapping(episode, chapter))


def test_mapping_repository_does_not_commit(session, graph):
    episode, chapter = persist_installments(session, graph)
    repo = EpisodeChapterMappingRepository(session)
    repo.add(EpisodeChapterMapping(episode, chapter))
    session.rollback()
    assert session.query(EpisodeChapterMappingORM).count() == 0
