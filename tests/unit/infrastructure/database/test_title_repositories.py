"""Tests for Series, AnimeTitle, and MangaTitle repositories."""

from collections.abc import Iterator

import pytest
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session, sessionmaker

from animemangadb.domain.entities import AnimeTitle, MangaTitle, Series
from animemangadb.domain.value_objects.canonical_title import CanonicalTitle
from animemangadb.domain.value_objects.slug import Slug
from animemangadb.infrastructure.database.base import Base
from animemangadb.infrastructure.database.models import (
    AnimeTitleORM,
    MangaTitleORM,
    SeriesORM,
)
from animemangadb.infrastructure.database.repositories import (
    AnimeTitleRepository,
    MangaTitleRepository,
    Repository,
    SeriesRepository,
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


def make_series(title: str = "One Piece") -> Series:
    return Series(title=CanonicalTitle(title))


def persist_series(session: Session, title: str = "One Piece") -> Series:
    series = make_series(title)
    SeriesRepository(session).add(series)
    session.flush()
    return series


def test_title_repositories_inherit_repository():
    assert issubclass(SeriesRepository, Repository)
    assert issubclass(AnimeTitleRepository, Repository)
    assert issubclass(MangaTitleRepository, Repository)


def test_series_repository_adds_without_commit(session: Session):
    repository = SeriesRepository(session)
    series = make_series()

    returned = repository.add(series)

    assert returned is series
    assert session.scalar(select(SeriesORM)) is not None
    assert session.in_transaction()


def test_series_repository_gets_by_slug(session: Session):
    repository = SeriesRepository(session)
    repository.add(make_series())
    session.flush()

    restored = repository.get_by_slug(Slug("one-piece"))

    assert isinstance(restored, Series)
    assert restored.title == CanonicalTitle("One Piece")


def test_series_repository_gets_by_title(session: Session):
    repository = SeriesRepository(session)
    repository.add(make_series())
    session.flush()

    restored = repository.get_by_title(CanonicalTitle("One Piece"))

    assert restored is not None
    assert restored.slug == Slug("one-piece")


def test_series_repository_returns_none_for_missing_rows(session: Session):
    repository = SeriesRepository(session)

    assert repository.get_by_slug(Slug("missing")) is None
    assert repository.get_by_title(CanonicalTitle("Missing")) is None


def test_series_repository_exists_and_lists_in_insert_order(session: Session):
    repository = SeriesRepository(session)
    repository.add(make_series("One Piece"))
    repository.add(make_series("Naruto"))
    session.flush()

    restored = repository.list_all()

    assert repository.exists_by_slug(Slug("one-piece"))
    assert not repository.exists_by_slug(Slug("bleach"))
    assert [item.title.value for item in restored] == ["One Piece", "Naruto"]


def test_series_repository_delete_stages_removal(session: Session):
    repository = SeriesRepository(session)
    series = make_series()
    repository.add(series)
    session.flush()

    assert repository.delete(series)
    session.flush()
    assert repository.get_by_slug(series.slug) is None
    assert not repository.delete(series)


def test_series_repository_rejects_wrong_types(session: Session):
    repository = SeriesRepository(session)

    with pytest.raises(TypeError):
        repository.add("One Piece")
    with pytest.raises(TypeError):
        repository.get_by_slug("one-piece")
    with pytest.raises(TypeError):
        repository.get_by_title("One Piece")


def test_anime_title_repository_adds_using_persisted_parent(session: Session):
    series = persist_series(session)
    title = AnimeTitle(series=series, title=CanonicalTitle("One Piece"))
    repository = AnimeTitleRepository(session)

    returned = repository.add(title)
    session.flush()
    orm_object = session.scalar(select(AnimeTitleORM))

    assert returned is title
    assert orm_object is not None
    assert orm_object.series.slug == "one-piece"


def test_anime_title_repository_requires_persisted_parent(session: Session):
    title = AnimeTitle(
        series=make_series(),
        title=CanonicalTitle("One Piece"),
    )

    with pytest.raises(LookupError):
        AnimeTitleRepository(session).add(title)


def test_anime_title_repository_gets_and_composes_parent(session: Session):
    series = persist_series(session)
    repository = AnimeTitleRepository(session)
    repository.add(AnimeTitle(series, CanonicalTitle("One Piece")))
    session.flush()

    restored = repository.get_by_slug(series.slug, Slug("one-piece"))

    assert isinstance(restored, AnimeTitle)
    assert restored.series.title == CanonicalTitle("One Piece")
    assert restored.title == CanonicalTitle("One Piece")


def test_anime_title_repository_gets_by_title(session: Session):
    series = persist_series(session)
    repository = AnimeTitleRepository(session)
    repository.add(AnimeTitle(series, CanonicalTitle("One Piece TV")))
    session.flush()

    restored = repository.get_by_title(
        series.slug,
        CanonicalTitle("One Piece TV"),
    )

    assert restored is not None
    assert restored.slug == Slug("one-piece-tv")


def test_anime_title_repository_scopes_duplicate_slugs_by_series(session: Session):
    one_piece = persist_series(session, "One Piece")
    remake = persist_series(session, "One Piece Remake")
    repository = AnimeTitleRepository(session)
    repository.add(AnimeTitle(one_piece, CanonicalTitle("The One Piece")))
    repository.add(AnimeTitle(remake, CanonicalTitle("The One Piece")))
    session.flush()

    first = repository.get_by_slug(one_piece.slug, Slug("the-one-piece"))
    second = repository.get_by_slug(remake.slug, Slug("the-one-piece"))

    assert first is not None and first.series.slug == one_piece.slug
    assert second is not None and second.series.slug == remake.slug


def test_anime_title_repository_exists_lists_and_deletes(session: Session):
    series = persist_series(session)
    repository = AnimeTitleRepository(session)
    first = AnimeTitle(series, CanonicalTitle("One Piece"))
    second = AnimeTitle(series, CanonicalTitle("One Piece Specials"))
    repository.add(first)
    repository.add(second)
    session.flush()

    assert repository.exists_by_slug(series.slug, first.slug)
    assert [item.title.value for item in repository.list_for_series(series.slug)] == [
        "One Piece",
        "One Piece Specials",
    ]
    assert repository.delete(first)
    session.flush()
    assert not repository.exists_by_slug(series.slug, first.slug)


def test_anime_title_repository_returns_empty_results(session: Session):
    repository = AnimeTitleRepository(session)

    assert repository.get_by_slug(Slug("missing"), Slug("missing")) is None
    assert repository.list_for_series(Slug("missing")) == []


def test_anime_title_repository_rejects_wrong_types(session: Session):
    repository = AnimeTitleRepository(session)

    with pytest.raises(TypeError):
        repository.add("One Piece")
    with pytest.raises(TypeError):
        repository.get_by_slug("series", Slug("title"))
    with pytest.raises(TypeError):
        repository.get_by_title(Slug("series"), "Title")


def test_manga_title_repository_adds_using_persisted_parent(session: Session):
    series = persist_series(session)
    title = MangaTitle(series=series, title=CanonicalTitle("One Piece"))
    repository = MangaTitleRepository(session)

    returned = repository.add(title)
    session.flush()
    orm_object = session.scalar(select(MangaTitleORM))

    assert returned is title
    assert orm_object is not None
    assert orm_object.series.slug == "one-piece"


def test_manga_title_repository_requires_persisted_parent(session: Session):
    title = MangaTitle(
        series=make_series(),
        title=CanonicalTitle("One Piece"),
    )

    with pytest.raises(LookupError):
        MangaTitleRepository(session).add(title)


def test_manga_title_repository_gets_and_composes_parent(session: Session):
    series = persist_series(session)
    repository = MangaTitleRepository(session)
    repository.add(MangaTitle(series, CanonicalTitle("One Piece")))
    session.flush()

    restored = repository.get_by_slug(series.slug, Slug("one-piece"))

    assert isinstance(restored, MangaTitle)
    assert restored.series.title == CanonicalTitle("One Piece")
    assert restored.title == CanonicalTitle("One Piece")


def test_manga_title_repository_gets_by_title(session: Session):
    series = persist_series(session)
    repository = MangaTitleRepository(session)
    repository.add(MangaTitle(series, CanonicalTitle("One Piece Manga")))
    session.flush()

    restored = repository.get_by_title(
        series.slug,
        CanonicalTitle("One Piece Manga"),
    )

    assert restored is not None
    assert restored.slug == Slug("one-piece-manga")


def test_manga_title_repository_scopes_duplicate_slugs_by_series(session: Session):
    first_series = persist_series(session, "One Piece")
    second_series = persist_series(session, "One Piece Color")
    repository = MangaTitleRepository(session)
    repository.add(MangaTitle(first_series, CanonicalTitle("One Piece")))
    repository.add(MangaTitle(second_series, CanonicalTitle("One Piece")))
    session.flush()

    first = repository.get_by_slug(first_series.slug, Slug("one-piece"))
    second = repository.get_by_slug(second_series.slug, Slug("one-piece"))

    assert first is not None and first.series.slug == first_series.slug
    assert second is not None and second.series.slug == second_series.slug


def test_manga_title_repository_exists_lists_and_deletes(session: Session):
    series = persist_series(session)
    repository = MangaTitleRepository(session)
    first = MangaTitle(series, CanonicalTitle("One Piece"))
    second = MangaTitle(series, CanonicalTitle("One Piece Color"))
    repository.add(first)
    repository.add(second)
    session.flush()

    assert repository.exists_by_slug(series.slug, first.slug)
    assert [item.title.value for item in repository.list_for_series(series.slug)] == [
        "One Piece",
        "One Piece Color",
    ]
    assert repository.delete(first)
    session.flush()
    assert not repository.exists_by_slug(series.slug, first.slug)


def test_manga_title_repository_returns_empty_results(session: Session):
    repository = MangaTitleRepository(session)

    assert repository.get_by_slug(Slug("missing"), Slug("missing")) is None
    assert repository.list_for_series(Slug("missing")) == []


def test_manga_title_repository_rejects_wrong_types(session: Session):
    repository = MangaTitleRepository(session)

    with pytest.raises(TypeError):
        repository.add("One Piece")
    with pytest.raises(TypeError):
        repository.get_by_slug("series", Slug("title"))
    with pytest.raises(TypeError):
        repository.get_by_title(Slug("series"), "Title")
