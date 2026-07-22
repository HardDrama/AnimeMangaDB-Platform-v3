"""Tests for the Domain and ORM mapping strategy."""

from dataclasses import FrozenInstanceError
from pathlib import Path

import pytest

from animemangadb.infrastructure.database import (
    DEFAULT_MAPPING_POLICY,
    MappingPolicy,
)


REPOSITORY_ROOT = Path(__file__).resolve().parents[4]
STRATEGY_DOCUMENT = (
    REPOSITORY_ROOT
    / "docs"
    / "specifications"
    / "database"
    / "MAPPING_STRATEGY.md"
)


def test_default_mapping_policy_is_mapping_policy():
    assert isinstance(
        DEFAULT_MAPPING_POLICY,
        MappingPolicy,
    )


def test_mapping_policy_is_immutable():
    with pytest.raises(FrozenInstanceError):
        DEFAULT_MAPPING_POLICY.map_relationships = True


def test_default_policy_maps_scalar_fields():
    assert DEFAULT_MAPPING_POLICY.map_scalar_fields is True


def test_default_policy_uses_shallow_relationship_mapping():
    assert DEFAULT_MAPPING_POLICY.map_relationships is False


def test_default_policy_does_not_preserve_database_identity():
    assert (
        DEFAULT_MAPPING_POLICY.preserve_persistence_identity
        is False
    )


def test_default_policy_assigns_graph_composition_to_repositories():
    assert (
        DEFAULT_MAPPING_POLICY.repository_composes_object_graphs
        is True
    )


def test_mapping_strategy_document_exists():
    assert STRATEGY_DOCUMENT.is_file()


def test_mapping_strategy_documents_required_rules():
    document = STRATEGY_DOCUMENT.read_text(
        encoding="utf-8",
    )

    required_statements = (
        "Every concrete entity mapper performs shallow conversion.",
        "Repositories own object-graph composition.",
        "A mapper must never recursively invoke a mapper",
        "Episode and Chapter identifiers remain strings",
        "database queries inside mappers",
        "SQLAlchemy imports inside the Domain Layer",
    )

    for statement in required_statements:
        assert statement in document
