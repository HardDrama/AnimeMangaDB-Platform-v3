import os

from animemangadb.infrastructure.database import (
    DATABASE_URL_ENVIRONMENT_VARIABLE,
    DEFAULT_SQLITE_URL,
    DatabaseConfig,
    load_database_config,
)


def test_default_database_url(monkeypatch):
    monkeypatch.delenv(
        DATABASE_URL_ENVIRONMENT_VARIABLE,
        raising=False,
    )

    config = load_database_config()

    assert config.database_url == DEFAULT_SQLITE_URL


def test_environment_database_url(monkeypatch):
    monkeypatch.setenv(
        DATABASE_URL_ENVIRONMENT_VARIABLE,
        "sqlite:///test.db",
    )

    config = load_database_config()

    assert (
        config.database_url
        == "sqlite:///test.db"
    )


def test_returns_database_config():
    config = load_database_config()

    assert isinstance(
        config,
        DatabaseConfig,
    )


def test_database_config_is_immutable():
    config = load_database_config()

    try:
        config.database_url = "other"
        mutated = True
    except Exception:
        mutated = False

    assert mutated is False


def test_environment_variable_name():
    assert (
        DATABASE_URL_ENVIRONMENT_VARIABLE
        == "ANIMEMANGADB_DATABASE_URL"
    )


def test_default_sqlite_url():
    assert (
        DEFAULT_SQLITE_URL
        == "sqlite:///animemangadb.db"
    )


def test_database_url_is_string():
    config = load_database_config()

    assert isinstance(
        config.database_url,
        str,
    )


def test_loading_configuration_does_not_modify_environment():
    before = dict(os.environ)

    load_database_config()

    after = dict(os.environ)

    assert before == after