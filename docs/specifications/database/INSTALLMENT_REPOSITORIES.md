# Installment Repositories

Version: v0.5.9C

## Purpose

The installment repository layer provides Domain-facing persistence operations for `Episode`, `Chapter`, and `EpisodeChapterMapping` while keeping SQLAlchemy objects inside infrastructure.

## Repositories

### EpisodeRepository

Scopes episode identity by:

- parent Series slug
- parent AnimeTitle slug
- `InstallmentIdentifier`

It stages additions and deletions, resolves persisted AnimeTitle parents, reconstructs the full Series → AnimeTitle → Episode Domain graph, and never commits.

### ChapterRepository

Scopes chapter identity by:

- parent Series slug
- parent MangaTitle slug
- `InstallmentIdentifier`

It stages additions and deletions, resolves persisted MangaTitle parents, reconstructs the full Series → MangaTitle → Chapter Domain graph, and never commits.

### EpisodeChapterMappingRepository

Resolves both persisted installment branches before staging an atomic mapping. It supports exact lookup, existence checks, episode-scoped lists, chapter-scoped lists, and staged deletion.

Returned mappings contain fully reconstructed Domain graphs on both sides. The mapper remains shallow; graph composition belongs to the repository.

## Ordering

Repository list methods use persistence insertion order (`id`). Installment identifiers remain strings and are not coerced into numeric values. This avoids inventing ordering rules for identifiers such as `12.5`, `OVA-2`, `SP1`, and `EX`.

## Transaction Boundary

All repositories receive an existing SQLAlchemy `Session`. They may stage, query, flush indirectly through the caller, and compose graphs. They do not commit, roll back, close, or create Sessions.

## Identity Boundary

Persistence IDs are internal implementation details. Public repository operations use Domain entities and value objects.
