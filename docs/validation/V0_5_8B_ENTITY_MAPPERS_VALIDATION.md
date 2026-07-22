# v0.5.8B Entity Mappers Validation

## Objective

Complete and certify the Entity Mapper checkpoint by implementing
shallow Domain ↔ ORM conversion for Episode, Chapter, and
EpisodeChapterMapping.

## Branch

```text
feature/v0.5.0-database-foundation
```

## Files Created

```text
src/animemangadb/infrastructure/database/mappers/episode_mapper.py
src/animemangadb/infrastructure/database/mappers/chapter_mapper.py
src/animemangadb/infrastructure/database/mappers/episode_chapter_mapping_mapper.py
tests/unit/infrastructure/database/test_installment_mappers.py
docs/specifications/database/INSTALLMENT_ENTITY_MAPPERS.md
docs/validation/V0_5_8B_ENTITY_MAPPERS_VALIDATION.md
PACKAGE_MANIFEST.md
RELEASE_NOTES.md
```

## Files Modified

```text
src/animemangadb/infrastructure/database/mappers/__init__.py
```

## Behavior Validated

- Episode scalar and parent conversion
- Chapter scalar and parent conversion
- Atomic Episode–Chapter relationship conversion
- InstallmentIdentifier reconstruction
- Non-numeric identifier preservation
- New unattached ORM object creation
- No persistence-ID copying
- No input mutation
- No recursive relationship mapping
- Persisted slug integrity validation
- Complete concrete mapper exports

## Expected Test Totals

```text
Previous validated total: 159
New tests:                 20
Expected total:           179
```

## Validation Commands and Results

### Focused Package B tests

```powershell
python -m pytest tests/unit/infrastructure/database/test_installment_mappers.py -q
```

Result:

```text
20 passed
```

### Complete mapper tests

```powershell
python -m pytest tests/unit/infrastructure/database/test_title_mappers.py tests/unit/infrastructure/database/test_installment_mappers.py -q
```

Result:

```text
36 passed
```

### Database infrastructure tests

```powershell
python -m pytest tests/unit/infrastructure/database -q
```

Result:

```text
93 passed
```

### Infrastructure suite

```powershell
python -m pytest tests/unit/infrastructure -q
```

Result:

```text
93 passed
```

### Complete unit suite

```powershell
python -m pytest tests/unit -q
```

Result:

```text
179 passed
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
179 passed
```

## Review Checklist

- [x] EpisodeMapper is implemented
- [x] ChapterMapper is implemented
- [x] EpisodeChapterMappingMapper is implemented
- [x] Concrete mappers inherit from Mapper
- [x] Parent and related context is explicit
- [x] Installment identifiers remain strings
- [x] No mapper performs queries
- [x] New ORM objects are unattached
- [x] Persistence IDs are not copied
- [x] Relationship collections are not recursively mapped
- [x] Slug integrity is validated
- [x] Focused Package B tests pass
- [x] Complete mapper tests pass
- [x] Database tests pass
- [x] Infrastructure tests pass
- [x] Unit suite passes
- [x] Ruff passes
- [x] Complete suite passes

## Certification

Status: Validated

Version: v0.5.8B

Full checkpoint: v0.5.8 Entity Mappers

Certification status: Certified
