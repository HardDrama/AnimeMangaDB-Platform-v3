# v0.3.0 — Domain Specification Validation

## Purpose

Certify the authoritative Platform v3 domain model before implementation begins.

## Scope

This checkpoint defines domain terminology, aggregate boundaries, core entities, relationships, ownership, identity, validation, lifecycle, invariants, future expansion, change control, and initial Architecture Decision Records.

This checkpoint does not add domain implementation classes.

## Files added

- `docs/specifications/domain/DOMAIN_SPECIFICATION.md`
- `docs/specifications/domain/adr/ADR-0001-series-is-the-aggregate-root.md`
- `docs/specifications/domain/adr/ADR-0002-anime-and-manga-are-sibling-branches.md`
- `docs/specifications/domain/adr/ADR-0003-episode-chapter-links-use-explicit-mappings.md`
- `docs/specifications/domain/adr/ADR-0004-domain-drives-the-architecture.md`
- `tests/unit/test_domain_specification_docs.py`

## Automated validation

Focused documentation tests:

```powershell
python -m pytest tests/unit/test_domain_specification_docs.py -q
```

Expected: `4 passed`

All unit tests:

```powershell
python -m pytest tests/unit -q
```

Ruff:

```powershell
python -m ruff check .
```

Complete suite:

```powershell
python -m pytest -q
```

All regression commands must report no failures and no errors.

## Manual domain review

Confirm the specification answers:

- What is a Series?
- Why is Series the aggregate root?
- Can a Series contain multiple Anime Titles? Yes
- Can a Series contain multiple Manga Titles? Yes
- What owns Episodes? Anime Titles
- What owns Chapters? Manga Titles
- Can Episodes and Chapters exist without mappings? Yes
- Can a Chapter map to Episodes from multiple Anime Titles? Yes
- Can an Episode map to Chapters from multiple Manga Titles? Yes
- How are Episode-Chapter relationships represented?
- What makes each entity unique?
- Are cross-Series mappings allowed? No
- Are non-integer local identifiers supported?
- Which future media types are anticipated?
- How must future domain changes be approved? Requires documentation and an ADR.

## Validation record

- Focused documentation tests: 4 passed
- Complete unit tests: 8 passed
- Ruff: all checks passed
- Complete suite: 8 passed
- Manual domain review: Complete
- Contradictions found: 0
- Corrections required: 1
- Corrections completed: 1

## Certification criteria

v0.3.0 may be certified only when:

1. All automated checks pass.
2. All required entities are defined.
3. Ownership is acyclic.
4. Identity rules are explicit.
5. Mapping invariants are explicit.
6. The four initial ADRs are accepted.
7. No unresolved contradictions remain.
8. The roadmap and changelog are updated.

## Certification

Status: Certified
