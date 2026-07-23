"""
Installment Repository Protocol Tests

Feature Checkpoint
v0.6.4
"""

from animemangadb.infrastructure.database.repositories import (
    ChapterRepository,
    EpisodeRepository,
)


def test_episode_repository_exposes_required_query_methods():
    required_methods = (
        "get_by_identifier",
        "exists_by_identifier",
        "list_for_anime_title",
    )

    for method in required_methods:
        assert hasattr(EpisodeRepository, method)


def test_chapter_repository_exposes_required_query_methods():
    required_methods = (
        "get_by_identifier",
        "exists_by_identifier",
        "list_for_manga_title",
    )

    for method in required_methods:
        assert hasattr(ChapterRepository, method)