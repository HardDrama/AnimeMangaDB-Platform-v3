"""
Episode-Chapter Mapping Repository Protocol Tests

Feature Checkpoint
v0.6.5
"""

from animemangadb.infrastructure.database.repositories import (
    EpisodeChapterMappingRepository,
)
from animemangadb.services.protocols import (
    EpisodeChapterMappingRepositoryProtocol,
)


def test_mapping_repository_exposes_required_query_methods():
    required_methods = (
        "get",
        "exists",
        "list_for_episode",
        "list_for_chapter",
    )

    for method in required_methods:
        assert hasattr(
            EpisodeChapterMappingRepository,
            method,
        )


def test_mapping_repository_protocol_declares_required_query_methods():
    required_methods = (
        "get",
        "exists",
        "list_for_episode",
        "list_for_chapter",
    )

    for method in required_methods:
        assert hasattr(
            EpisodeChapterMappingRepositoryProtocol,
            method,
        )