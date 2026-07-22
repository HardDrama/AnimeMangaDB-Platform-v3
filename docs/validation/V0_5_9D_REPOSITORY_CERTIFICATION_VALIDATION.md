# v0.5.9D Repository Certification Validation

## Purpose
Certify the repository layer as one integrated persistence boundary.

## Scope
- Repository foundation
- Title repositories
- Installment repositories
- Cross-session graph reconstruction
- Shared transaction ownership
- Rollback behavior
- Domain/persistence identity separation
- Parent-scoped installment identity
- Public repository exports

## Installation
Copy `tests/` and `docs/` into the project root. No production source files are replaced.

## Validation
Run each command separately and stop on any failure or warning.

```powershell
python -m pytest tests/unit/infrastructure/database/test_repository_certification.py -q
```
Expected: `8 passed`

```powershell
python -m pytest tests/unit/infrastructure/database/test_repository_foundation.py tests/unit/infrastructure/database/test_title_repositories.py tests/unit/infrastructure/database/test_installment_repositories.py tests/unit/infrastructure/database/test_repository_certification.py -q
```
Expected: `76 passed`

```powershell
python -m pytest tests/unit/infrastructure/database -q
```
Expected: `169 passed`

```powershell
python -m pytest tests/unit/infrastructure -q
```
Expected: `169 passed`

```powershell
python -m pytest tests/unit -q
```
Expected: `255 passed`

```powershell
python -m ruff check .
```
Expected: `All checks passed`

```powershell
python -m pytest -q
```
Expected: `255 passed`

## Certification criteria
v0.5.9D is certified when all commands pass without warnings and the changes are committed.
