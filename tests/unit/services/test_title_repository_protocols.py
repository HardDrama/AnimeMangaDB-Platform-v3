"""
Title Repository Protocol Tests

Feature Checkpoint
v0.6.3
"""

from animemangadb.infrastructure.database.repositories import (
    AnimeTitleRepository,
    MangaTitleRepository,
)


def test_anime_title_repository_exposes_required_query_methods():
    required_methods = (
        "get_by_slug",
        "get_by_title",
        "exists_by_slug",
        "list_for_series",
    )

    for method in required_methods:
        assert hasattr(
            AnimeTitleRepository,
            method,
        )


def test_manga_title_repository_exposes_required_query_methods():
    required_methods = (
        "get_by_slug",
        "get_by_title",
        "exists_by_slug",
        "list_for_series",
    )

    for method in required_methods:
        assert hasattr(
            MangaTitleRepository,
            method,
        )