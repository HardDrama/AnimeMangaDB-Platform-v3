from pathlib import Path

import animemangadb


def test_backend_package_uses_src_layout():
    package_path = Path(animemangadb.__file__).resolve().parent
    assert package_path.name == "animemangadb"
    assert package_path.parent.name == "src"


def test_frontend_is_not_a_backend_subpackage():
    package_path = Path(animemangadb.__file__).resolve().parent
    assert not (package_path / "frontend").exists()


def test_expected_backend_packages_exist():
    package_path = Path(animemangadb.__file__).resolve().parent
    expected_packages = {
        "api", "config", "data", "domain",
        "ingestion", "services", "tools",
    }
    actual_packages = {
        path.name
        for path in package_path.iterdir()
        if path.is_dir() and (path / "__init__.py").exists()
    }
    assert expected_packages.issubset(actual_packages)
