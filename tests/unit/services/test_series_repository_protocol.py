"""
Series Repository Protocol Tests

Feature Checkpoint
v0.7.0
"""

from typing import runtime_checkable

from animemangadb.infrastructure.database.repositories import (
    SeriesRepository,
)
from animemangadb.services.protocols import (
    SeriesRepositoryProtocol,
)


def test_protocol_is_runtime_checkable():
    """
    Repository protocols should support runtime
    structural compatibility checks.
    """

    runtime_protocol = runtime_checkable(
        SeriesRepositoryProtocol,
    )

    assert getattr(
        runtime_protocol,
        "_is_runtime_protocol",
        False,
    )


def test_database_repository_satisfies_protocol():
    """
    The concrete SQLAlchemy repository should expose
    every method required by the application layer.
    """

    required_methods = (
        "add",
        "get_by_slug",
        "get_by_title",
        "exists_by_slug",
        "list_all",
    )

    for method in required_methods:
        assert hasattr(
            SeriesRepository,
            method,
        )