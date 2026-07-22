"""
Tests for the Platform v3 database package foundation.
"""

import ast
import importlib
from pathlib import Path


def repository_root() -> Path:
    """Return the repository root directory."""
    return Path(__file__).resolve().parents[4]


def test_infrastructure_package_can_be_imported():
    module = importlib.import_module(
        "animemangadb.infrastructure"
    )

    assert module is not None


def test_database_package_can_be_imported():
    module = importlib.import_module(
        "animemangadb.infrastructure.database"
    )

    assert module is not None


def test_persistence_strategy_document_exists():
    strategy_document = (
        repository_root()
        / "docs"
        / "specifications"
        / "database"
        / "PERSISTENCE_STRATEGY.md"
    )

    assert strategy_document.is_file()


def test_persistence_strategy_documents_core_boundaries():
    strategy_document = (
        repository_root()
        / "docs"
        / "specifications"
        / "database"
        / "PERSISTENCE_STRATEGY.md"
    )

    content = strategy_document.read_text(
        encoding="utf-8"
    )

    required_statements = (
        "Domain entities and ORM persistence models will be separate classes.",
        "InstallmentIdentifier must remain a string in persistence.",
        "Repositories will return domain entities rather than ORM models.",
        "episode_id + chapter_id",
        "SQLAlchemy imports inside the Domain Layer",
    )

    for statement in required_statements:
        assert statement in content


def test_domain_layer_does_not_import_infrastructure():
    root = repository_root()
    domain_root = (
        root
        / "src"
        / "animemangadb"
        / "domain"
    )

    violations: list[str] = []

    for source_file in domain_root.rglob("*.py"):
        syntax_tree = ast.parse(
            source_file.read_text(encoding="utf-8"),
            filename=str(source_file),
        )

        for node in ast.walk(syntax_tree):
            imported_modules: list[str] = []

            if isinstance(node, ast.Import):
                imported_modules.extend(
                    alias.name
                    for alias in node.names
                )

            if (
                isinstance(node, ast.ImportFrom)
                and node.module is not None
            ):
                imported_modules.append(node.module)

            for imported_module in imported_modules:
                if imported_module.startswith(
                    "animemangadb.infrastructure"
                ):
                    relative_path = source_file.relative_to(
                        root
                    )
                    violations.append(
                        f"{relative_path}: {imported_module}"
                    )

    assert violations == [], (
        "The Domain Layer must not depend on "
        f"Infrastructure: {violations}"
    )