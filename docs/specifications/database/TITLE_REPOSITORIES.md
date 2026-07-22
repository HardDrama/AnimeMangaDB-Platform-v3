# v0.5.9B — Title Repositories

## Scope

This checkpoint introduces concrete repositories for the title branch of the Domain model:

- `SeriesRepository`
- `AnimeTitleRepository`
- `MangaTitleRepository`

The repositories sit between application services and SQLAlchemy. They accept and return Domain entities and value objects; ORM rows remain infrastructure details.

## Repository responsibilities

The title repositories:

- receive an injected SQLAlchemy `Session`;
- map Domain entities to ORM rows;
- reconstruct Domain entities from ORM rows;
- resolve parent `Series` rows for anime and manga titles;
- compose parent Domain objects when reading child titles;
- query by business identity;
- stage inserts and deletes without committing;
- preserve persistence identifiers inside the infrastructure layer.

They do not:

- create, commit, roll back, or close Sessions;
- expose ORM rows through public methods;
- copy database IDs into Domain entities;
- recursively delegate graph composition to mappers.

## Public operations

### SeriesRepository

- `add(series)`
- `get_by_slug(slug)`
- `get_by_title(title)`
- `exists_by_slug(slug)`
- `list_all()`
- `delete(series)`

### AnimeTitleRepository

- `add(anime_title)`
- `get_by_slug(series_slug, slug)`
- `get_by_title(series_slug, title)`
- `exists_by_slug(series_slug, slug)`
- `list_for_series(series_slug)`
- `delete(anime_title)`

### MangaTitleRepository

- `add(manga_title)`
- `get_by_slug(series_slug, slug)`
- `get_by_title(series_slug, title)`
- `exists_by_slug(series_slug, slug)`
- `list_for_series(series_slug)`
- `delete(manga_title)`

## Business identity

`Series` is located by its globally unique slug.

`AnimeTitle` and `MangaTitle` are located by the combination of:

1. parent Series slug; and
2. title slug or canonical title.

This mirrors the database uniqueness boundary and avoids treating infrastructure IDs as Domain identity.

## Parent resolution

Adding an anime or manga title requires its parent Series to already be persistent in the current database transaction. If no matching Series row exists, the repository raises `LookupError`.

Repositories, not mappers, perform this resolution. The shallow mapper policy remains unchanged.

## Transaction boundary

All writes are staged in the injected Session. The application boundary remains responsible for `commit()` or `rollback()`.
