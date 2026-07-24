"""
Application Service Foundation Certification Tests

Feature Checkpoint
v0.6.7

These tests certify the complete current application-service foundation.

Certification Gates

- Query Service Inventory
- Repository Protocol Dependency
- Read-Only Query Boundary
- Transaction Responsibility
- Persistence Boundary
- Layer Dependency Boundary
"""

import ast
import inspect
from pathlib import Path

from animemangadb.services.protocols import TransactionProtocol


SERVICES_ROOT = (
    Path(__file__).resolve().parents[3]
    / "src"
    / "animemangadb"
    / "services"
)

QUERIES_ROOT = SERVICES_ROOT / "queries"

EXPECTED_QUERY_SERVICES = {
    "anime_title_queries.py": (
        "AnimeTitleQueryService",
        "AnimeTitleRepositoryProtocol",
    ),
    "chapter_queries.py": (
        "ChapterQueryService",
        "ChapterRepositoryProtocol",
    ),
    "episode_queries.py": (
        "EpisodeQueryService",
        "EpisodeRepositoryProtocol",
    ),
    "manga_title_queries.py": (
        "MangaTitleQueryService",
        "MangaTitleRepositoryProtocol",
    ),
    "mapping_queries.py": (
        "EpisodeChapterMappingQueryService",
        "EpisodeChapterMappingRepositoryProtocol",
    ),
    "series_queries.py": (
        "SeriesQueryService",
        "SeriesRepositoryProtocol",
    ),
}

FORBIDDEN_IMPORT_PREFIXES = (
    "sqlalchemy",
    "fastapi",
    "animemangadb.api",
    "animemangadb.infrastructure",
    "animemangadb.ingestion",
)

MUTATION_METHOD_NAMES = {
    "add",
    "commit",
    "create",
    "delete",
    "flush",
    "insert",
    "remove",
    "rollback",
    "save",
    "update",
}

FORBIDDEN_PERSISTENCE_CALLS = {
    "add",
    "commit",
    "delete",
    "execute",
    "flush",
    "merge",
    "rollback",
}


def parse_python_file(path: Path) -> ast.Module:
    """
    Parse one Python source file.
    """

    return ast.parse(
        path.read_text(encoding="utf-8"),
        filename=str(path),
    )


def iter_service_python_files() -> list[Path]:
    """
    Return every Python source file in the services package.
    """

    return sorted(SERVICES_ROOT.rglob("*.py"))


def iter_query_python_files() -> list[Path]:
    """
    Return every concrete query-service source file.
    """

    return sorted(
        path
        for path in QUERIES_ROOT.glob("*.py")
        if path.name != "__init__.py"
    )


def imported_modules(tree: ast.Module) -> set[str]:
    """
    Return the modules imported by one parsed source file.
    """

    modules: set[str] = set()

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            modules.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            modules.add(node.module)

    return modules


def imported_names(tree: ast.Module) -> set[str]:
    """
    Return names imported with from-import statements.
    """

    names: set[str] = set()

    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom):
            names.update(alias.name for alias in node.names)

    return names


def annotation_name(annotation: ast.expr | None) -> str | None:
    """
    Return the final name represented by a type annotation.
    """

    if annotation is None:
        return None

    if isinstance(annotation, ast.Name):
        return annotation.id

    if isinstance(annotation, ast.Attribute):
        return annotation.attr

    if isinstance(annotation, ast.Constant) and isinstance(
        annotation.value,
        str,
    ):
        return annotation.value

    return None


def find_class(tree: ast.Module, class_name: str) -> ast.ClassDef | None:
    """
    Find one top-level class by name.
    """

    for node in tree.body:
        if isinstance(node, ast.ClassDef) and node.name == class_name:
            return node

    return None


def test_expected_query_services_are_present():
    actual_files = {
        path.name
        for path in iter_query_python_files()
    }

    assert actual_files == set(EXPECTED_QUERY_SERVICES)


def test_query_services_depend_on_expected_repository_protocols():
    violations: list[str] = []

    for filename, (
        service_name,
        protocol_name,
    ) in EXPECTED_QUERY_SERVICES.items():
        path = QUERIES_ROOT / filename
        tree = parse_python_file(path)
        service_class = find_class(tree, service_name)

        if service_class is None:
            violations.append(
                f"{filename}: missing {service_name}",
            )
            continue

        names = imported_names(tree)

        if protocol_name not in names:
            violations.append(
                f"{filename}: does not import {protocol_name}",
            )

        constructor = next(
            (
                node
                for node in service_class.body
                if isinstance(
                    node,
                    (ast.FunctionDef, ast.AsyncFunctionDef),
                )
                and node.name == "__init__"
            ),
            None,
        )

        if constructor is None:
            violations.append(
                f"{filename}: {service_name} has no constructor",
            )
            continue

        parameter_annotations = {
            annotation_name(argument.annotation)
            for argument in constructor.args.args
            if argument.arg != "self"
        }

        if protocol_name not in parameter_annotations:
            violations.append(
                f"{filename}: constructor does not depend on "
                f"{protocol_name}",
            )

    assert violations == []


def test_query_services_expose_no_mutation_operations():
    violations: list[str] = []

    for filename, (
        service_name,
        _,
    ) in EXPECTED_QUERY_SERVICES.items():
        path = QUERIES_ROOT / filename
        tree = parse_python_file(path)
        service_class = find_class(tree, service_name)

        if service_class is None:
            continue

        for node in service_class.body:
            if not isinstance(
                node,
                (ast.FunctionDef, ast.AsyncFunctionDef),
            ):
                continue

            if node.name in MUTATION_METHOD_NAMES:
                violations.append(
                    f"{filename}: {service_name}.{node.name}",
                )

    assert violations == []


def test_query_services_do_not_control_transactions_or_sessions():
    violations: list[str] = []

    for path in iter_query_python_files():
        tree = parse_python_file(path)
        relative_path = path.relative_to(SERVICES_ROOT)

        if "TransactionProtocol" in imported_names(tree):
            violations.append(
                f"{relative_path}: imports TransactionProtocol",
            )

        for node in ast.walk(tree):
            if isinstance(node, ast.Name) and node.id in {
                "Session",
                "sessionmaker",
                "create_engine",
            }:
                violations.append(
                    f"{relative_path}: references {node.id}",
                )

            if (
                isinstance(node, ast.Call)
                and isinstance(node.func, ast.Attribute)
                and node.func.attr in FORBIDDEN_PERSISTENCE_CALLS
            ):
                violations.append(
                    f"{relative_path}: calls {node.func.attr}()",
                )

    assert violations == []


def test_transaction_protocol_is_available_for_future_command_services():
    public_methods = {
        name
        for name, member in inspect.getmembers(
            TransactionProtocol,
            predicate=inspect.isfunction,
        )
        if not name.startswith("_")
    }

    assert public_methods == {
        "commit",
        "rollback",
    }


def test_application_services_have_no_forbidden_layer_dependencies():
    violations: list[str] = []

    for path in iter_service_python_files():
        tree = parse_python_file(path)
        relative_path = path.relative_to(SERVICES_ROOT)

        for module in imported_modules(tree):
            if module.startswith(FORBIDDEN_IMPORT_PREFIXES):
                violations.append(
                    f"{relative_path}: {module}",
                )

    assert violations == []