# v0.5.7 Mapping Strategy Validation

## Objective

Define and certify the conversion rules that concrete Domain ↔ ORM mappers
will follow.

## Branch

```text
feature/v0.5.0-database-foundation
```

## Files Created

```text
src/animemangadb/infrastructure/database/mappers/strategy.py
docs/specifications/database/MAPPING_STRATEGY.md
tests/unit/infrastructure/database/test_mapping_strategy.py
docs/validation/V0_5_7_MAPPING_STRATEGY_VALIDATION.md
```

## Files Modified

```text
src/animemangadb/infrastructure/database/mappers/__init__.py
src/animemangadb/infrastructure/database/__init__.py
```

## Strategy Certified

- Entity mappers perform shallow scalar conversion.
- Mappers do not recursively traverse relationships.
- Repositories compose object graphs.
- Mappers perform no database queries.
- ORM primary keys remain persistence-only identity.
- Episode and Chapter identifiers remain strings.
- Domain → ORM conversion creates new unattached ORM objects.
- ORM → Domain conversion creates new framework-independent objects.
- The default mapping policy is immutable.

## Intentionally Not Introduced

- Concrete entity mappers
- Repositories
- Database queries
- Persistence operations
- Aggregate loading behavior

## Validation Commands and Results

### Focused mapping-strategy tests

```powershell
python -m pytest tests/unit/infrastructure/database/test_mapping_strategy.py -q
```

Result:

```text
8 passed
```

### Database infrastructure tests

```powershell
python -m pytest tests/unit/infrastructure/database -q
```

Result:

```text
57 passed
```

### Infrastructure suite

```powershell
python -m pytest tests/unit/infrastructure -q
```

Result:

```text
57 passed
```

### Complete unit suite

```powershell
python -m pytest tests/unit -q
```

Result:

```text
143 passed
```

### Static analysis

```powershell
python -m ruff check .
```

Result:

```text
all checks passed
```

### Complete project suite

```powershell
python -m pytest -q
```

Result:

```text
143 passed
```

## Review Checklist

- [x] MappingPolicy exists
- [x] MappingPolicy is immutable
- [x] Scalar mapping is enabled
- [x] Relationship mapping is disabled
- [x] Persistence identity is not copied into Domain entities
- [x] Repositories own graph composition
- [x] Mapping strategy document exists
- [x] Recursion rules are documented
- [x] Identifier preservation is documented
- [x] Prohibited mapper behavior is documented
- [x] Focused tests pass
- [x] Infrastructure tests pass
- [x] Unit suite passes
- [x] Ruff passes
- [x] Complete suite passes

## Certification

Status: Certified

Certified version: v0.5.7

Certified checkpoint: Mapping Strategy
