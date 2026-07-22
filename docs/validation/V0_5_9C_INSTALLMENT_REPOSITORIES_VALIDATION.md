# v0.5.9C Installment Repositories Validation

## Installation

Copy the package's `src/`, `tests/`, and `docs/` folders into the repository root. Copy `PACKAGE_MANIFEST.md` and `RELEASE_NOTES.md` to the root when maintaining package records.

The package adds three repository modules and updates `repositories/__init__.py`. Do not delete `base.py` or the v0.5.9B title repositories.

## Focused Validation

```powershell
python -m pytest tests/unit/infrastructure/database/test_installment_repositories.py -q
```

Expected:

```text
32 passed
```

## Repository Regression Validation

```powershell
python -m pytest tests/unit/infrastructure/database/test_repository_foundation.py tests/unit/infrastructure/database/test_title_repositories.py tests/unit/infrastructure/database/test_installment_repositories.py -q
```

Expected:

```text
68 passed
```

## Database Validation

```powershell
python -m pytest tests/unit/infrastructure/database -q
```

Expected:

```text
161 passed
```

## Infrastructure Validation

```powershell
python -m pytest tests/unit/infrastructure -q
```

Expected:

```text
161 passed
```

## Unit Validation

```powershell
python -m pytest tests/unit -q
```

Expected:

```text
247 passed
```

## Static Analysis

```powershell
python -m ruff check .
```

Expected:

```text
All checks passed!
```

## Full Project Validation

```powershell
python -m pytest -q
```

Expected:

```text
247 passed
```

## Regression Checks

Confirm that:

- production `Base.metadata` still contains only the six certified ORM tables;
- v0.5.9A repository foundation tests remain green;
- v0.5.9B title repository tests remain green;
- mapper tests remain green;
- repositories do not commit implicitly;
- installment identifiers remain strings;
- relationship graphs are reconstructed by repositories rather than mappers;
- focused validation emits no warnings.

## Local Package Evidence

The focused v0.5.9C suite was executed against the uploaded source snapshot with the certified v0.5.9B package overlaid:

```text
32 passed
```

The uploaded snapshot omitted two older documentation files required by existing tests (`PERSISTENCE_STRATEGY.md` and `MAPPING_STRATEGY.md`). Therefore, complete local regression totals could not be certified in the isolated build environment. The user's complete repository remains the source of truth for final validation.
