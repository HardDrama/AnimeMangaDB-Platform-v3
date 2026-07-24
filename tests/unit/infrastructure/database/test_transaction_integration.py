"""
Transaction Boundary Integration Tests

Feature Checkpoint
v0.6.6
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from animemangadb.domain.entities import (
    AnimeTitle,
    Series,
)
from animemangadb.domain.value_objects.canonical_title import (
    CanonicalTitle,
)
from animemangadb.infrastructure.database import (
    SQLAlchemyTransaction,
)
from animemangadb.infrastructure.database.base import Base
from animemangadb.infrastructure.database.repositories import (
    AnimeTitleRepository,
    SeriesRepository,
)


def test_shared_transaction_commits_multiple_repository_changes():
    """
    One transaction commits work staged by multiple repositories.
    """
    engine = create_engine("sqlite+pysqlite:///:memory:")
    Base.metadata.create_all(engine)
    factory = sessionmaker(
        bind=engine,
        expire_on_commit=False,
    )

    series = Series(
        CanonicalTitle("One Piece"),
    )
    anime_title = AnimeTitle(
        series,
        CanonicalTitle("One Piece Anime"),
    )

    with factory() as first_session:
        series_repository = SeriesRepository(first_session)
        anime_title_repository = AnimeTitleRepository(
            first_session,
        )
        transaction = SQLAlchemyTransaction(first_session)

        series_repository.add(series)
        first_session.flush()

        anime_title_repository.add(anime_title)

        transaction.commit()

    with factory() as second_session:
        restored_series = SeriesRepository(
            second_session,
        ).get_by_slug(
            series.slug,
        )
        restored_anime_title = AnimeTitleRepository(
            second_session,
        ).get_by_slug(
            series.slug,
            anime_title.slug,
        )

        assert restored_series is not None
        assert restored_anime_title is not None
        assert restored_series.title == series.title
        assert restored_anime_title.title == anime_title.title
        assert (
            restored_anime_title.series.slug
            == restored_series.slug
        )

    Base.metadata.drop_all(engine)
    engine.dispose()


def test_shared_transaction_rolls_back_multiple_repository_changes():
    """
    One transaction discards work staged by multiple repositories.
    """
    engine = create_engine("sqlite+pysqlite:///:memory:")
    Base.metadata.create_all(engine)
    factory = sessionmaker(
        bind=engine,
        expire_on_commit=False,
    )

    series = Series(
        CanonicalTitle("One Piece"),
    )
    anime_title = AnimeTitle(
        series,
        CanonicalTitle("One Piece Anime"),
    )

    with factory() as first_session:
        series_repository = SeriesRepository(first_session)
        anime_title_repository = AnimeTitleRepository(
            first_session,
        )
        transaction = SQLAlchemyTransaction(first_session)

        series_repository.add(series)
        first_session.flush()

        anime_title_repository.add(anime_title)
        first_session.flush()

        transaction.rollback()

    with factory() as second_session:
        restored_series = SeriesRepository(
            second_session,
        ).get_by_slug(
            series.slug,
        )
        restored_anime_title = AnimeTitleRepository(
            second_session,
        ).get_by_slug(
            series.slug,
            anime_title.slug,
        )

        assert restored_series is None
        assert restored_anime_title is None

    Base.metadata.drop_all(engine)
    engine.dispose()