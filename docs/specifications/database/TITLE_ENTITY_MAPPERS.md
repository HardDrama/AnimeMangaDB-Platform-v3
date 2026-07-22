# Title Entity Mappers

## Scope

v0.5.8A implements shallow mapping for:

- `Series`
- `AnimeTitle`
- `MangaTitle`

These mappers follow the mapping strategy certified in v0.5.7.

## Shared Value-Object Conversion

`helpers.py` centralizes conversion between Domain value objects and
ORM-compatible primitive strings.

Package A includes helpers for:

- `CanonicalTitle`
- `Slug`
- `InstallmentIdentifier`

Installment identifier helpers are included now so Package B can use
the same conversion boundary without duplication.

## SeriesMapper

`SeriesMapper.to_orm(series)` creates a new, unattached `SeriesORM`
containing:

- `title`
- `slug`

`SeriesMapper.to_domain(series_orm)` reconstructs:

- `CanonicalTitle`
- the Domain-derived `Slug`

Persistence IDs and relationship collections are not copied.

## Parent-Dependent Title Mappers

`AnimeTitle` and `MangaTitle` require a `Series` in their Domain
constructors. Their ORM models also require a parent Series
relationship for persistence.

Repositories therefore resolve the parent before invoking a mapper.

Domain conversion:

```python
AnimeTitleMapper.to_domain(
    anime_title_orm,
    series=resolved_series,
)
```

ORM conversion:

```python
AnimeTitleMapper.to_orm(
    anime_title,
    series_orm=resolved_series_orm,
)
```

The same rule applies to `MangaTitleMapper`.

This explicit parent context is not recursive graph mapping. The
mapper receives an already-resolved parent and performs no queries.

## Slug Integrity

Domain entities derive their slug from the canonical title.

During ORM → Domain conversion, the mapper verifies that the
persisted slug matches the Domain-derived slug. A mismatch raises
`ValidationError`, identifying inconsistent persisted state instead
of silently changing it.

## Prohibited Behavior

Title entity mappers do not:

- create database Sessions;
- execute queries;
- add or commit ORM objects;
- copy persistence primary keys into Domain entities;
- recursively map parent or child graphs;
- mutate input objects;
- expose SQLAlchemy objects through Domain types.

## Package Boundary

v0.5.8A is an implementation package within the larger v0.5.8
checkpoint. The complete Entity Mapper checkpoint is certified only
after v0.5.8B implements and validates installment-level mappers.
