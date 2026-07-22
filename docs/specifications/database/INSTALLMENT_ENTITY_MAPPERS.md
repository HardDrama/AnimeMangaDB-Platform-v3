# Installment Entity Mappers

## Scope

v0.5.8B completes concrete shallow mapping for:

- `Episode`
- `Chapter`
- `EpisodeChapterMapping`

Together with v0.5.8A, this completes the Entity Mapper checkpoint.

## EpisodeMapper

The mapper converts:

- `InstallmentIdentifier` ↔ persisted `str`
- `CanonicalTitle` ↔ persisted `str`
- Domain-derived `Slug` → persisted `str`

Repositories provide the resolved parent:

```python
EpisodeMapper.to_domain(
    episode_orm,
    anime_title=resolved_anime_title,
)
```

```python
EpisodeMapper.to_orm(
    episode,
    anime_title_orm=resolved_anime_title_orm,
)
```

Chapter mapping relationships are intentionally ignored.

## ChapterMapper

The mapper follows the same rules with a resolved `MangaTitle` or
`MangaTitleORM` parent.

Episode mapping relationships are intentionally ignored.

## EpisodeChapterMappingMapper

The mapping entity contains no scalar business fields. It represents
one atomic relationship between an Episode and a Chapter.

Repositories resolve both sides before invoking the mapper:

```python
EpisodeChapterMappingMapper.to_domain(
    mapping_orm,
    episode=resolved_episode,
    chapter=resolved_chapter,
)
```

```python
EpisodeChapterMappingMapper.to_orm(
    mapping,
    episode_orm=resolved_episode_orm,
    chapter_orm=resolved_chapter_orm,
)
```

The mapper does not recursively convert either branch.

## Identifier Preservation

Installment identifiers remain strings through persistence.

The mapper therefore preserves identifiers such as:

- `1130`
- `12.5`
- `OVA-2`
- `SP1`
- `EX`

No numeric coercion or ordering rule belongs in the mapper layer.

## Integrity Rules

During ORM → Domain conversion, EpisodeMapper and ChapterMapper
validate that persisted slugs match slugs derived by Domain entities
from canonical titles.

A mismatch raises the Domain `ValidationError`.

## Prohibited Behavior

Installment mappers do not:

- open Sessions;
- execute queries;
- add, flush, or commit ORM objects;
- copy persistence primary keys into Domain entities;
- recursively map parent or relationship graphs;
- coerce installment identifiers to numbers;
- mutate mapper inputs.

## Repository Boundary

Repositories remain responsible for:

- locating parent rows;
- resolving related Domain entities;
- composing complete object graphs;
- selecting identity and persistence behavior;
- controlling transaction boundaries.
