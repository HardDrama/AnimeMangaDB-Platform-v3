# v0.4.7 Installment Entities Validation

## Objective

Implement the Episode and Chapter entities.

## Files Created

```text
src/animemangadb/domain/entities/episode.py
src/animemangadb/domain/entities/chapter.py
tests/unit/domain/entities/test_episode.py
tests/unit/domain/entities/test_chapter.py
docs/validation/V0_4_7_INSTALLMENT_ENTITIES_VALIDATION.md
```

## Files Modified

```text
src/animemangadb/domain/entities/__init__.py
```

## Implemented Behavior

- Episode belongs to AnimeTitle.
- Chapter belongs to MangaTitle.
- Episode requires InstallmentIdentifier.
- Chapter requires InstallmentIdentifier.
- Episode requires CanonicalTitle.
- Chapter requires CanonicalTitle.
- Slugs are derived automatically.
- Entities remain infrastructure independent.

## Certification

Status: Certified