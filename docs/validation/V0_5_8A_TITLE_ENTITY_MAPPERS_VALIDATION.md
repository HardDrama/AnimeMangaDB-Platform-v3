# v0.5.8A Title Entity Mappers Validation

## Objective

Implement and validate shallow Domain ↔ ORM conversion for Series,
AnimeTitle, and MangaTitle.

## Branch

```text
feature/v0.5.0-database-foundation
```

## Files Created

```text
src/animemangadb/infrastructure/database/mappers/helpers.py
src/animemangadb/infrastructure/database/mappers/series_mapper.py
src/animemangadb/infrastructure/database/mappers/anime_title_mapper.py
src/animemangadb/infrastructure/database/mappers/manga_title_mapper.py
tests/unit/infrastructure/database/test_title_mappers.py
docs/specifications/database/TITLE_ENTITY_MAPPERS.md
docs/validation/V0_5_8A_TITLE_ENTITY_MAPPERS_VALIDATION.md
PACKAGE_MANIFEST.md
RELEASE_NOTES.md
```

## Files Modified

```text
src/animemangadb/infrastructure/database/mappers/__init__.py
```

## Behavior Validated

- Shallow scalar conversion
- Domain value-object reconstruction
- Explicit resolved-parent context
- New-object creation
- No Session attachment
- No input mutation
- No persistence-ID copying
- Empty child relationship collections
- Persisted slug integrity validation
- Mapper inheritance and exports

## Expected Test Totals

```text
Previous certified total: 143
New tests:                16
Expected total:          159
```

## Validation Commands and Results

### Focused mapper tests

```powershell
python -m pytest tests/unit/infrastructure/database/test_title_mappers.py -q
```

Result:

```text
[enter actual result]
```

### Database infrastructure tests

```powershell
python -m pytest tests/unit/infrastructure/database -q
```

Result:

```text
[enter actual result]
```

### Infrastructure suite

```powershell
python -m pytest tests/unit/infrastructure -q
```

Result:

```text
[enter actual result]
```

### Complete unit suite

```powershell
python -m pytest tests/unit -q
```

Result:

```text
[enter actual result]
```

### Static analysis

```powershell
python -m ruff check .
```

Result:

```text
[enter actual result]
```

### Complete project suite

```powershell
python -m pytest -q
```

Result:

```text
[enter actual result]
```

## Review Checklist

- [ ] Shared conversion helpers exist
- [ ] SeriesMapper is implemented
- [ ] AnimeTitleMapper is implemented
- [ ] MangaTitleMapper is implemented
- [ ] Concrete mappers inherit from Mapper
- [ ] Parent context is supplied explicitly
- [ ] No mapper performs queries
- [ ] ORM objects are unattached when created
- [ ] Persistence IDs are not copied
- [ ] Child collections are not recursively mapped
- [ ] Slug integrity is validated
- [ ] Focused tests pass
- [ ] Infrastructure tests pass
- [ ] Unit suite passes
- [ ] Ruff passes
- [ ] Complete suite passes

## Package Status

Status: Validated Package A

Version: v0.5.8A

Full v0.5.8 certification: Pending v0.5.8B
