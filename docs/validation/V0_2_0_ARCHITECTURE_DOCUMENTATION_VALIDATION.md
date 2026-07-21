# v0.2.0 — Architecture Documentation Validation

## Purpose

Certify the Platform v3 architecture, package boundaries, and dependency direction before domain implementation begins.

## Changes

- Added the Platform v3 architecture specification.
- Added explicit dependency rules.
- Made backend directories importable Python packages.
- Established the frontend as a separate top-level application.
- Added package-boundary tests.

## Validation commands

```powershell
python -m pytest tests/unit/test_package_boundaries.py -q
python -m pytest tests/unit -q
python -m ruff check .
python -m pytest -q
```

Expected:

- focused boundary tests: `3 passed`
- no failures or errors
- Ruff: `All checks passed!`

## Manual validation

Confirm:

- `frontend/` exists at the repository root.
- `src/animemangadb/frontend/` does not exist.
- The architecture document reflects the agreed series-first tree.
- Episodes and chapters are sibling branches.
- Their relationship is an explicit mapping.
- API and frontend responsibilities are separated.

## Validation record

- Focused boundary tests: 3 passed
- Complete unit tests: 4 passed
- Ruff: all checks passed
- Complete suite: 4 passed
- Manual architecture review:

## Certification

Status: Certified
