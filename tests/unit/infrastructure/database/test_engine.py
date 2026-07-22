from sqlalchemy.engine import Engine

from animemangadb.infrastructure.database import (
    create_database_engine,
)


def test_create_database_engine_returns_engine():
    engine = create_database_engine()

    assert isinstance(
        engine,
        Engine,
    )


def test_engine_url_matches_configuration():
    engine = create_database_engine()

    assert (
        str(engine.url)
        == "sqlite:///animemangadb.db"
    )


def test_engine_has_metadata():
    engine = create_database_engine()

    assert engine.dialect is not None


def test_engine_creation_is_repeatable():
    first = create_database_engine()
    second = create_database_engine()

    assert isinstance(first, Engine)
    assert isinstance(second, Engine)