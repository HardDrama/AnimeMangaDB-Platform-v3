"""
Application Services Foundation Tests

Feature Checkpoint
v0.6.0
"""

import ast
from pathlib import Path

from animemangadb.services import ApplicationServiceError


SERVICES_ROOT = (
    Path(__file__).resolve().parents[3]
    / "src"
    / "animemangadb"
    / "services"
)

FORBIDDEN_IMPORT_PREFIXES = (
    "sqlalchemy",
    "fastapi",
    "animemangadb.api",
    "animemangadb.infrastructure",
    "animemangadb.ingestion",
)


def iter_service_python_files() -> list[Path]:
    """
    Return every Python source file in the application-services package.
    """

    return sorted(SERVICES_ROOT.rglob("*.py"))


def imported_modules(path: Path) -> set[str]:
    """
    Return modules imported by one Python source file.
    """

    tree = ast.parse(
        path.read_text(encoding="utf-8"),
        filename=str(path),
    )

    modules: set[str] = set()

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            modules.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            modules.add(node.module)

    return modules


def test_application_service_error_is_publicly_importable():
    assert issubclass(
        ApplicationServiceError,
        Exception,
    )


def test_application_service_error_has_no_infrastructure_parent():
    assert ApplicationServiceError.__bases__ == (Exception,)


def test_application_services_package_contains_expected_foundation():
    expected_paths = {
        SERVICES_ROOT / "__init__.py",
        SERVICES_ROOT / "exceptions.py",
        SERVICES_ROOT / "protocols" / "__init__.py",
        SERVICES_ROOT / "queries" / "__init__.py",
    }

    assert expected_paths.issubset(
        set(iter_service_python_files()),
    )


def test_application_services_do_not_import_forbidden_layers():
    violations: list[str] = []

    for path in iter_service_python_files():
        for module in imported_modules(path):
            if module.startswith(FORBIDDEN_IMPORT_PREFIXES):
                relative_path = path.relative_to(SERVICES_ROOT)
                violations.append(
                    f"{relative_path}: {module}",
                )

    assert violations == []


def test_application_services_do_not_define_transport_or_orm_types():
    forbidden_base_names = {
        "BaseModel",
        "DeclarativeBase",
        "APIRouter",
    }
    violations: list[str] = []

    for path in iter_service_python_files():
        tree = ast.parse(
            path.read_text(encoding="utf-8"),
            filename=str(path),
        )

        for node in ast.walk(tree):
            if not isinstance(node, ast.ClassDef):
                continue

            for base in node.bases:
                if isinstance(base, ast.Name):
                    base_name = base.id
                elif isinstance(base, ast.Attribute):
                    base_name = base.attr
                else:
                    continue

                if base_name in forbidden_base_names:
                    relative_path = path.relative_to(SERVICES_ROOT)
                    violations.append(
                        f"{relative_path}: {node.name} -> {base_name}",
                    )

    assert violations == []