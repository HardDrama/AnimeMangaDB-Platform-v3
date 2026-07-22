# v0.5.9B Title Repositories — Validation

## Local package validation

The focused test module was executed against the uploaded v0.5.9A source snapshot:

```powershell
python -m pytest tests/unit/infrastructure/database/test_title_repositories.py -q
```

Observed result:

```text
24 passed
```

The uploaded snapshot did not include the existing documentation tree required by four older tests. Therefore, a complete local regression run against that snapshot could not be certified here. Those failures were missing-file failures for the pre-existing `PERSISTENCE_STRATEGY.md` and `MAPPING_STRATEGY.md`, not failures caused by v0.5.9B.

## Installation

1. Confirm the current branch is `feature/v0.5.0-database-foundation`.
2. Extract the package.
3. Copy the package `src/` directory into the repository root.
4. Copy the package `tests/` directory into the repository root.
5. Copy the package `docs/` directory into the repository root.
6. Copy `PACKAGE_MANIFEST.md` and `RELEASE_NOTES.md` into the repository root, replacing the prior checkpoint copies when prompted.
7. Verify the repository directory contains:

```text
base.py
series_repository.py
anime_title_repository.py
manga_title_repository.py
__init__.py
```

## Validation sequence

### 1. Focused repository tests

```powershell
python -m pytest tests/unit/infrastructure/database/test_title_repositories.py -q
```

Expected:

```text
24 passed
```

### 2. Repository layer tests

```powershell
python -m pytest tests/unit/infrastructure/database/test_repository_foundation.py tests/unit/infrastructure/database/test_title_repositories.py -q
```

Expected:

```text
36 passed
```

### 3. Database regression suite

```powershell
python -m pytest tests/unit/infrastructure/database -q
```

Expected:

```text
129 passed
```

### 4. Infrastructure regression suite

```powershell
python -m pytest tests/unit/infrastructure -q
```

Expected:

```text
129 passed
```

### 5. Unit suite

```powershell
python -m pytest tests/unit -q
```

Expected:

```text
215 passed
```

### 6. Static analysis

```powershell
python -m ruff check .
```

Expected:

```text
All checks passed!
```

### 7. Full project suite

```powershell
python -m pytest -q
```

Expected:

```text
215 passed
```

## Regression checks

Confirm that:

- production `Base.metadata` still contains only the six certified ORM tables;
- all title mapper tests remain green;
- repository foundation tests remain green;
- repositories do not commit implicitly;
- child title reads reconstruct their parent Series;
- identical child slugs can exist under different Series;
- missing parents raise `LookupError`;
- no persistence IDs enter Domain objects.

## Stop conditions

Stop validation and report the complete output if:

- any focused test fails;
- expected metadata changes;
- a repository performs an implicit commit;
- Ruff reports an error;
- any prior regression test fails.

## Commit

Commit only after every validation command passes.

Suggested commit message:

```text
v0.5.9B - Implement title repositories
```
