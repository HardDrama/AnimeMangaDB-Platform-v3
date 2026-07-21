from pathlib import Path


DOMAIN_ROOT = (
    Path(__file__).resolve().parents[2]
    / "docs"
    / "specifications"
    / "domain"
)


def test_master_domain_specification_exists():
    specification = DOMAIN_ROOT / "DOMAIN_SPECIFICATION.md"

    assert specification.is_file()


def test_master_specification_contains_required_sections():
    specification = (
        DOMAIN_ROOT / "DOMAIN_SPECIFICATION.md"
    ).read_text(encoding="utf-8")

    required_sections = {
        "## 3. Domain philosophy",
        "## 4. Terminology",
        "## 5. Aggregate root",
        "## 6. Entity definitions",
        "## 7. Relationship model",
        "## 8. Ownership rules",
        "## 9. Identity rules",
        "## 10. Validation rules",
        "## 11. Lifecycle rules",
        "## 12. Domain invariants",
        "## 14. Future expansion",
        "## 16. Change control",
    }

    for section in required_sections:
        assert section in specification


def test_initial_domain_adrs_exist_and_are_accepted():
    adr_root = DOMAIN_ROOT / "adr"

    expected_adrs = {
        "ADR-0001-series-is-the-aggregate-root.md",
        "ADR-0002-anime-and-manga-are-sibling-branches.md",
        "ADR-0003-episode-chapter-links-use-explicit-mappings.md",
        "ADR-0004-domain-drives-the-architecture.md",
    }

    actual_adrs = {
        path.name
        for path in adr_root.glob("ADR-*.md")
    }

    assert expected_adrs.issubset(actual_adrs)

    for adr_name in expected_adrs:
        content = (adr_root / adr_name).read_text(
            encoding="utf-8"
        )
        assert "## Status" in content
        assert "Accepted" in content
        assert "## Context" in content
        assert "## Decision" in content
        assert "## Consequences" in content


def test_domain_specification_defines_core_entities():
    specification = (
        DOMAIN_ROOT / "DOMAIN_SPECIFICATION.md"
    ).read_text(encoding="utf-8")

    entities = {
        "## 6.1 Series",
        "## 6.2 Anime Title",
        "## 6.3 Episode",
        "## 6.4 Manga Title",
        "## 6.5 Chapter",
        "## 6.6 Episode-Chapter Mapping",
    }

    for entity in entities:
        assert entity in specification
